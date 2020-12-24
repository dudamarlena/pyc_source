# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\bmccs\Desktop\streamml2\streamml2\streamline\transformation\AbstractTransformer.py
# Compiled at: 2019-01-19 21:05:43
# Size of source mod 2**32: 186 bytes
import pandas as pd

class AbstractTransformer:

    def __init__(self, code):
        self.code = code

    def transform(self):
        pass