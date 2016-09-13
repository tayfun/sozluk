# -*- coding: utf-8 -*-
"""
Provides a translation method that strips Turkish characters and replaces
them with ASCII equivalents.
"""


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
