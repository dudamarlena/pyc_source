# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fever/reader/simple_random.py
# Compiled at: 2019-01-25 08:19:53
# Size of source mod 2**32: 518 bytes
import os, random

class SimpleRandom:
    instance = None

    def __init__(self, seed):
        self.seed = seed
        self.random = random.Random(seed)

    def next_rand(self, a, b):
        return self.random.randint(a, b)

    @staticmethod
    def get_instance():
        if SimpleRandom.instance is None:
            SimpleRandom.instance = SimpleRandom(SimpleRandom.get_seed())
        return SimpleRandom.instance

    @staticmethod
    def get_seed():
        return int(os.getenv('RANDOM_SEED', 1234))