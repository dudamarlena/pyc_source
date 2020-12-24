# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\evmcodegen\generators\distribution.py
# Compiled at: 2018-10-12 11:44:35
# Size of source mod 2**32: 1718 bytes
"""
Distribution based code generators
"""
import random
from ..utils.random import random_gauss, WeightedRandomizer
from .base import _BaseCodeGen

class DistrCodeGen(_BaseCodeGen):

    def __init__(self, distribution):
        super().__init__()
        self.type = _BaseCodeGen.TYPE_OPCODE_ONLY
        self.distribution = distribution

    def _frandom(self, distribution):
        return random.randrange(distribution.min, distribution.max)

    def generate(self, length=None):
        length = length or int(self._frandom(self.distribution))
        rnd_prolog = WeightedRandomizer(self.distribution.distribution_prolog)
        rnd_epilog = WeightedRandomizer(self.distribution.distribution)
        rnd_corpus = WeightedRandomizer(self.distribution.distribution_epilog)
        b = []
        for _ in range(128):
            b.append(rnd_prolog.random())

        for _ in range(length - 256):
            b.append(rnd_corpus.random())

        for _ in range(128):
            b.append(rnd_epilog.random())

        return bytes(b)


class GaussDistrCodeGen(DistrCodeGen):

    def _frandom(self, distribution):
        return random_gauss(distribution.avg, 0.1 * distribution.avg + distribution.min, bottom=distribution.min, top=distribution.max)