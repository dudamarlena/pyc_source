# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ycyc/libs/algorithms/hashlib/simhash.py
# Compiled at: 2016-05-26 01:47:38
import re

class SimHash(object):

    @classmethod
    def hash_of(cls, tokens, bits):
        """
        Return simhash for n bits by tokens.

        :param tokens: token with weight:[(weight, token), ...]
        :param bits: bits of simhash
        """
        v_range = tuple(range(bits))
        v_result = [ 0 for i in v_range ]
        for weight, word in tokens:
            word_hash = hash(word)
            bmask = 1
            for i in v_range:
                if word_hash & bmask:
                    v_result[i] += weight
                else:
                    v_result[i] -= weight
                bmask <<= 1

        return tuple((1 if i > 0 else 0) for i in v_result)

    def __init__(self, tokens, bits):
        self.hash_result = self.hash_of(tokens, bits)
        self.tokens = tokens
        self.bits = bits

    def raw(self):
        return int(('').join(str(i) for i in self.hash_result), 2)

    def hex(self):
        hex_step = 4
        hex_numbers = '0123456789ABCDEF'
        additional_bits = hex_step - self.bits % hex_step
        if additional_bits < hex_step:
            hash_result = [
             0] * additional_bits
        else:
            hash_result = []
        hash_result.extend(self.hash_result)
        str_result = []
        for i in range(0, self.bits, hex_step):
            nums = hash_result[i:i + hex_step]
            str_result.append(hex_numbers[reduce(lambda n, i: n << 1 | i, nums, 0)])

        return ('').join(str_result)


def simhash(words, bits=128, spliter=None):
    """
    Return simple simhash which weight all is 1 of each item.

    :param words: string words
    :param bits: bits of simhash
    :param spliter: spliter to split words
    """
    if spliter is not None:
        words = spliter(words)
    return SimHash(((1, i) for i in words), bits).raw()


class Spliter(object):

    @classmethod
    def by_space(cls, words):
        return words.split()

    @classmethod
    def by_sep(cls, seps):

        def wrapper(words):
            return words.split(seps)

        return wrapper

    @classmethod
    def by_punctuations(cls, words):
        return re.split('\\W', words)

    @classmethod
    def by_step(cls, step):

        def wrapper(words):
            word_len = len(words)
            start = 0
            end = step
            while start < word_len:
                yield words[start:end]
                start = end
                end += step

        return wrapper