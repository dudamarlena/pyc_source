# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\evmcodegen\utils\random.py
# Compiled at: 2018-10-10 14:37:32
# Size of source mod 2**32: 1082 bytes
import random, binascii

class WeightedRandomizer(object):

    def __init__(self, weights):
        self._WeightedRandomizer__max = 0.0
        self._WeightedRandomizer__weights = []
        for value, weight in weights.items():
            self._WeightedRandomizer__max += weight
            self._WeightedRandomizer__weights.append((self._WeightedRandomizer__max, value))

    def random(self):
        r = random.random() * self._WeightedRandomizer__max
        for ceil, value in self._WeightedRandomizer__weights:
            if ceil > r:
                return value


def random_gauss(mu, sigma, bottom=None, top=None):
    while 1:
        rndval = int(random.gauss(mu, sigma))
        if bottom is not None:
            if top is not None:
                if bottom <= rndval <= top:
                    break

    return rndval


def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))


def bytes_to_hexstr(b, prefix=''):
    return '%s%s' % (prefix, binascii.hexlify(b).decode('utf-8'))