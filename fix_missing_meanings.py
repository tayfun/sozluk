"""
Python 3 because this is not for lambda (don't be fooled by
__future__.print_function import below, that works in 3 too).
"""
from __future__ import print_function
from itertools import chain

import boto3

from encoding import normalize
from scrapers import scrape_meaning


dynamodb = boto3.resource('dynamodb')
dict_table = dynamodb.Table('dictionary')
entries_table = dynamodb.Table('entries')


def main():
    entries_to_check = set()
    LastEvaluatedKey = None
    while(True):
        scan_kwargs = {}
        if LastEvaluatedKey:
            scan_kwargs['ExclusiveStartKey'] = LastEvaluatedKey
        response = entries_table.scan(
            **scan_kwargs
        )
        items = response['Items']
        if not items:
            break
        LastEvaluatedKey = response['LastEvaluatedKey']
        # We can only request items by 100 chunks in batch_get_item.
        for chunk_start in xrange(0, len(items), 100):
            item_chunk = items[chunk_start:chunk_start+100]
            entries_in_entries = set(item['entry'] for item in item_chunk)
            add_norm_fields(item_chunk)
            response = dynamodb.batch_get_item(
                RequestItems={
                    'dictionary': {
                        'Keys': item_chunk,
                        'AttributesToGet': ['entry', 'sources'],
                    }
                }
            )
            assert not response['UnprocessedKeys'], "Should've processed all."
            entries_in_dictionary = set()
            for item in response['Responses']['dictionary']:
                if not item['sources']:
                    continue
                entries_in_dictionary.add(item['entry'])
            entries_to_check = entries_to_check.union(
                entries_in_entries.difference(entries_in_dictionary)
            )
            if len(entries_to_check) > 25:
                process_entries(entries_to_check)
        # We've reached the end of the table.
        if not LastEvaluatedKey:
            break
    # Process last entries < 10 that haven't been processed yet.
    process_entries(entries_to_check)


def add_norm_fields(items):
    for item in items:
        item['norm'] = normalize(item['entry'])


def process_entries(entries_to_check):
    with dict_table.batch_writer(overwrite_by_pkeys=['norm', 'entry']) as \
            dict_b, entries_table.batch_writer(overwrite_by_pkeys=['entry']) \
            as entry_b:
        for entry in entries_to_check:
            print('Processing {}'.format(entry))
            meaning = scrape_meaning(entry)
            if not meaning['sources']:
                print("ERROR: Couldn't find meaning for {}".format(entry))
                continue
            dict_b.put_item(Item=meaning)
            for related_entry in chain(
                    meaning['related_entries']['compound_entries'],
                    meaning['related_entries']['idioms']
            ):
                if related_entry:
                    entry_b.put_item(Item={'entry': related_entry})
    entries_to_check.clear()


if __name__ == '__main__':
    main()
