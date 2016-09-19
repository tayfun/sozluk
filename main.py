from itertools import chain

import boto3
from scrapers import scrape_meaning, get_entries_and_next_page

dynamodb = boto3.resource('dynamodb')

# TODO: For debugging only, comment when not needed.
import logging  # NOQA
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def add_meaning(event, context):
    """
    Insert meaning info to dictionary for each new entry.

    Entries are in `entries` DynamoDB table. This lambda handler is triggered
    on a change to `entries` table.
    """
    dict_table = dynamodb.Table('dictionary')
    entries_table = dynamodb.Table('entries')
    with dict_table.batch_writer(overwrite_by_pkeys=['norm', 'entry']) as \
            dict_b, entries_table.batch_writer(overwrite_by_pkeys=['entry']) \
            as entry_b:
        for record in event['Records']:
            # We're only interested in INSERT events.
            if record['eventName'] != 'INSERT':
                continue
            entry = record['dynamodb']['Keys']['entry']['S']
            meaning = scrape_meaning(entry)
            dict_b.put_item(Item=meaning)
            """
            Sometimes we get related entries that are not in the "writing
            guide" list that we scrape below to gather entries. So we need to
            add them here.
            """
            for related_entry in chain(
                    meaning['related_entries']['compound_entries'],
                    meaning['related_entries']['idioms']
            ):
                if related_entry:
                    entry_b.put_item(Item={'entry': related_entry})


def add_entries(event, context):
    """
    Insert entries to the `entries` table, scraped from urls.

    URLs to scrape are taken from `urls` DynamoDB table. This lambda handler
    is triggered on a change to `urls` table.
    """
    urls_table = dynamodb.Table('urls')
    entries_table = dynamodb.Table('entries')
    with entries_table.batch_writer(overwrite_by_pkeys=['entry']) as entry_b, \
            urls_table.batch_writer(overwrite_by_pkeys=['url']) as url_b:
        for record in event['Records']:
            # We're only interested in INSERT events.
            if record['eventName'] != 'INSERT':
                continue
            url = record['dynamodb']['Keys']['url']['S']
            entries, next_page = get_entries_and_next_page(url)
            """
            If you send a None as key, you'll get:

            An error occurred (ValidationException) when calling the
            BatchWriteItem operation: The provided key element does not match
            the schema
            """
            if next_page:
                url_b.put_item(Item={'url': next_page})
            for entry in entries:
                entry_b.put_item(Item={'entry': entry})
