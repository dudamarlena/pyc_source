# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tom/pyenv/py3/lib/python3.5/site-packages/test/base_test_class.py
# Compiled at: 2019-03-21 21:31:15
# Size of source mod 2**32: 227 bytes
import unittest, numpy as np

class Test(unittest.TestCase):
    seed = 9527

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self._rs = np.random.RandomState(self.seed)