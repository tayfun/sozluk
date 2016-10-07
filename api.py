# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import json

import boto3
from boto3.dynamodb.conditions import Key

from encoding import normalize

dynamodb = boto3.resource('dynamodb')
dict_table = dynamodb.Table('dictionary')


def get_meaning(event, context):
    """The handler API Gateway uses to get meaning."""
    entry_query = event.get('entry')
    norm = normalize(entry_query)
    response = dict_table.query(KeyConditionExpression=Key('norm').eq(norm))
    items = response.get('Items', [])
    if not items:
        raise ValueError('404')
    return items
