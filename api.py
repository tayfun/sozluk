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
    if not items:
        raise ValueError('404')
    return items


# Inlined here so all code is in a single file.
translate_table = {
    ord("ğ"): "g",
    ord("ü"): "u",
    ord("ş"): "s",
    ord("ı"): "i",
    ord("ö"): "o",
    ord("ç"): "c",
    ord("Ğ"): "G",
    ord("Ü"): "U",
    ord("Ş"): "S",
    ord("İ"): "I",
    ord("Ö"): "O",
    ord("Ç"): "C",
    ord("î"): "i",
    ord("Î"): "i",
    ord("â"): "a",
    ord("Â"): "a",
    ord("û"): "u",
    ord("Û"): "u",
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
