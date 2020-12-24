# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pynats2/nuid.py
# Compiled at: 2019-10-24 23:34:08
# Size of source mod 2**32: 2291 bytes
from random import Random, SystemRandom
from sys import maxsize as MaxInt
DIGITS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
BASE = 62
PREFIX_LENGTH = 12
SEQ_LENGTH = 10
TOTAL_LENGTH = PREFIX_LENGTH + SEQ_LENGTH
MAX_SEQ = BASE ** 10
MIN_INC = 33
MAX_INC = 333
INC = MAX_INC - MIN_INC

class NUID:
    """NUID"""

    def __init__(self) -> None:
        self._srand = SystemRandom()
        self._prand = Random(self._srand.randint(0, MaxInt))
        self._seq = self._prand.randint(0, MAX_SEQ)
        self._inc = MIN_INC + self._prand.randint(0, INC)
        self.randomize_prefix()

    def next_(self) -> bytearray:
        self._seq += self._inc
        if self._seq >= MAX_SEQ:
            self.randomize_prefix()
            self.reset_sequential()
        _seq = self._seq
        prefix = self._prefix[:]

        def _next():
            nonlocal _seq
            a = DIGITS[(int(_seq) % BASE)]
            _seq /= BASE
            return a

        suffix = bytearray(_next() for i in range(SEQ_LENGTH))
        prefix.extend(suffix)
        return prefix

    def randomize_prefix(self) -> None:
        random_bytes = (self._srand.getrandbits(8) for i in range(PREFIX_LENGTH))
        self._prefix = bytearray(DIGITS[(c % BASE)] for c in random_bytes)

    def reset_sequential(self) -> None:
        self._seq = self._prand.randint(0, MAX_SEQ)
        self._inc = MIN_INC + self._prand.randint(0, INC)