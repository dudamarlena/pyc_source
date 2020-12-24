# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/asyncee/python-obscene-words-filter/obscene_words_filter/regexp.py
# Compiled at: 2017-01-24 08:54:20
from __future__ import unicode_literals
import re
from functools import partial
alphabet_ru = {b'а': b'а', 
   b'б': b'б', 
   b'в': b'в', 
   b'г': b'г', 
   b'д': b'д', 
   b'е': b'е', 
   b'ё': b'ё', 
   b'ж': b'ж', 
   b'з': b'з', 
   b'и': b'и', 
   b'й': b'й', 
   b'к': b'к', 
   b'л': b'л', 
   b'м': b'м', 
   b'н': b'н', 
   b'о': b'о', 
   b'п': b'п', 
   b'р': b'р', 
   b'с': b'с', 
   b'т': b'т', 
   b'у': b'у', 
   b'ф': b'ф', 
   b'х': b'х', 
   b'ц': b'ц', 
   b'ч': b'ч', 
   b'ъ': b'ъ', 
   b'ы': b'ы', 
   b'ь': b'ь', 
   b'э': b'э', 
   b'ю': b'ю', 
   b'я': b'я'}

def variants_of_letter(alphabet, letter):
    letters = alphabet.get(letter, letter)
    return (b'|').join(letters.split())


ru_variants_of_letter = partial(variants_of_letter, alphabet_ru)

def build_bad_phrase(*symbols, **kwargs):
    u"""
    Построить регулярную фразу из символов.

    Между символами могут располагаться пробелы или любые не−кириллические символы.
    Фраза возвращается в виде группы.
    """
    variants_func = kwargs.get(b'variants_func', ru_variants_of_letter)
    separator = b'(?:[^а-я])*'
    if len(symbols) == 1:
        symbols = symbols[0].split()
    symbol_regexp = []
    for symbol in symbols:
        if len(symbol) == 1:
            symbol = [
             symbol]
        parts = [ variants_func(i) for i in symbol ]
        symbol_regexp.append((b'[{}]+').format((b'|').join(parts)))

    return (b'[а-я]*({})[а-я]*').format(separator.join(symbol_regexp))


def build_good_phrase(*symbols):
    if len(symbols) == 1:
        symbols = symbols[0].split()
    out = []
    for symbol in symbols:
        out.append((b'[{}]').format(symbol))

    return (b'({})').format((b'').join(out))