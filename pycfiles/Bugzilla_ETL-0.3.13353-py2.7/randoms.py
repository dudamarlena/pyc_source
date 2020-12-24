# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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