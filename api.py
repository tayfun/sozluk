# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import json

import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource('dynamodb')
dict_table = dynamodb.Table('dictionary')


def get_meaning(event, context):
    """The handler API Gateway uses to get meaning."""
    entry_query = event.get('entry')
    norm = normalize(entry_query)
    response = dict_table.query(KeyConditionExpression=Key('norm').eq(norm))
    items = response.get('Items', [])
    return json.dumps(items)


# Inlined here so all code is in a single file.
translate_table = {
    ord(u"ğ"): u"g",
    ord(u"ü"): u"u",
    ord(u"ş"): u"s",
    ord(u"ı"): u"i",
    ord(u"ö"): u"o",
    ord(u"ç"): u"c",
    ord(u"Ğ"): u"G",
    ord(u"Ü"): u"U",
    ord(u"Ş"): u"S",
    ord(u"İ"): u"I",
    ord(u"Ö"): u"O",
    ord(u"Ç"): u"C",
}


def normalize(s):
    """
    Transforms a unicode string so that it can be searched and found even when
    it is not exactly the same. So for example a user can search for "Oğlak"
    and we can find "oğlak" by normalizing both to "oglak".

    Lowercases all the letters and anglicanizes it.

    u"Oğlak"     => oglak
    u"başucu"    => basucu
    u"Noel Baba" => noel baba
    """
    s = s.lower()
    return s.translate(translate_table)
