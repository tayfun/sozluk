# -*- coding: utf-8 -*-
"""
Provides a translation method that strips Turkish characters and replaces
them with ASCII equivalents.
"""
from __future__ import print_function
from __future__ import unicode_literals


translate_table = {
    ord("â"): "a",
    ord("Â"): "a",
    ord("ç"): "c",
    ord("Ç"): "C",
    ord("ğ"): "g",
    ord("Ğ"): "g",
    ord("ı"): "i",
    ord("I"): "i",
    ord("î"): "i",
    # buyuk i harfi.
    ord("İ"): "i",
    # sapkali I
    ord("Î"): "i",
    ord("ş"): "s",
    ord("Ş"): "s",
    ord("ö"): "o",
    ord("Ö"): "o",
    ord("û"): "u",
    ord("Û"): "u",
    ord("ü"): "u",
    ord("Ü"): "u",
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
