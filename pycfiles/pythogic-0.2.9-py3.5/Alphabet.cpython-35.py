# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pythogic/base/Alphabet.py
# Compiled at: 2018-03-04 13:18:22
# Size of source mod 2**32: 296 bytes
from typing import Set
from pythogic.base.Symbol import Symbol

class Alphabet(object):

    def __init__(self, symbols: Set[Symbol]):
        self.symbols = symbols

    @staticmethod
    def fromStrings(symbol_strings: Set[str]):
        return Alphabet(set(Symbol(s) for s in symbol_strings))