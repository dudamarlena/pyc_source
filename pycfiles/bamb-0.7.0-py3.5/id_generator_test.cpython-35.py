# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/id_generator_test.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 408 bytes
import unittest
from service import utils

class IdGeneratorTest(unittest.TestCase):

    def setUp(self):
        utils.IdGenerator.setup({'global': -1, 'cat1': 1000})

    def tearDown(self):
        pass

    def test_get_next(self):
        self.assertEqual(utils.IdGenerator.next(), 0)
        self.assertEqual(utils.IdGenerator.next(), 1)
        self.assertEqual(utils.IdGenerator.next('cat1'), 1001)