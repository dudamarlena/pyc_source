# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\bzETL\util\randoms.py
# Compiled at: 2013-11-22 17:13:19
import random, string
SIMPLE_ALPHABET = string.ascii_letters + string.digits
SEED = random.Random()

class Random(object):

    @staticmethod
    def string(length, alphabet=SIMPLE_ALPHABET):
        result = ''
        for i in range(0, length):
            result += SEED.choice(alphabet)

        return result

    @staticmethod
    def hex(length):
        return Random.string(length, string.digits + 'ABCDEF')

    @staticmethod
    def int(*args):
        return random.randrange(*args)

    @staticmethod
    def sample(data, count):
        num = len(data)
        return [ data[Random.int(num)] for i in range(count) ]