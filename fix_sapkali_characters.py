"""
Fixes normalizing "sapkali" characters.
"""
from __future__ import print_function
from __future__ import unicode_literals

import boto3

from encoding import normalize


dynamodb = boto3.resource('dynamodb')
dict_table = dynamodb.Table('dictionary')


def main():
    LastEvaluatedKey = None
    print('Starting...')
    while True:
        scan_kwargs = {
            'ProjectionExpression': 'entry,norm'
        }
        if LastEvaluatedKey:
            scan_kwargs['ExclusiveStartKey'] = LastEvaluatedKey
        response = dict_table.scan(
            **scan_kwargs
        )
        items = response['Items']
        if not items:
            break
        LastEvaluatedKey = response.get('LastEvaluatedKey')
        for item in items:
            new_norm = normalize(item['entry'])
            if item['norm'] != new_norm:
                print("For entry {0}, change norm from {1} to {2}".format(
                    item['entry'], item['norm'], new_norm))
                """
                We cannot update primary key attribute
                (which norm is one of them, a sort key, so
                we have to get_item, delete old one and
                create new one. Below does not work.
                dict_table.update_item(
                    Key=item,
                    UpdateExpression='SET norm = :norm',
                    ExpressionAttributeValues={
                        ':norm': {'S': new_norm}
                    }
                )
                """
                whole_item = dict_table.get_item(Key=item)['Item']
                whole_item['norm'] = new_norm
                dict_table.delete_item(Key=item)
                dict_table.put_item(Item=whole_item)

if __name__ == '__main__':
    main()
