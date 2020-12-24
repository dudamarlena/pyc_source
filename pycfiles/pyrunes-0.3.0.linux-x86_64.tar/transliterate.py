# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yori/Envs/pyrunes/lib/python2.7/site-packages/runes/transliterate.py
# Compiled at: 2016-07-02 12:56:14
from __future__ import absolute_import, unicode_literals
from .runic_alphabets import get_alphabet
from .exceptions import TransliterationDoesNotExist

def to_runes(chars, runic_alphabet=b'elder_futhark', errors=b'strict'):
    runic_alphabet = get_alphabet(runic_alphabet)
    for char in chars:
        yield _get_key(runic_alphabet, char, errors)


def to_rune(char, runic_alphabet=b'elder_futhark', errors=b'strict'):
    runic_alphabet = get_alphabet(runic_alphabet)
    return _get_key(runic_alphabet, char, errors)


def from_runes(runes, runic_alphabet=b'elder_futhark', errors=b'strict'):
    runic_alphabet = get_alphabet(runic_alphabet).inv
    for rune in runes:
        yield _get_key(runic_alphabet, rune, errors)


def from_rune(rune, runic_alphabet=b'elder_futhark', errors=b'strict'):
    runic_alphabet = get_alphabet(runic_alphabet)
    return _get_key(runic_alphabet.inv, rune, errors)


def _get_key(dic, key, errors=b'strict'):
    try:
        return dic[key]
    except KeyError:
        if errors == b'strict':
            raise TransliterationDoesNotExist((b'The transliteration of "{key}" does not exist.').format(key=key))
        return b''