# -*- coding: utf-8 -*-
"""
Provides a translation method that strips Turkish characters and replaces
them with ASCII equivalents.
"""
from __future__ import print_function
from __future__ import unicode_literals


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
