# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ifacetools\fbtest\numpv.py
# Compiled at: 2019-08-12 20:51:57
# Size of source mod 2**32: 448 bytes
from faker import Faker
from faker.providers import BaseProvider
import random
fake = Faker()

class NumProvider(BaseProvider):

    def num(self):
        ri = self.randomInt()
        return str(ri())

    def randomInt(self):
        return lambda a=1, b=30: random.randint(a, b)