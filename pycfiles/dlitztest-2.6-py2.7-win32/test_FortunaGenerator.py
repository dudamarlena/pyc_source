# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Random\Fortuna\test_FortunaGenerator.py
# Compiled at: 2013-03-13 13:15:35
"""Self-tests for Crypto.Random.Fortuna.FortunaGenerator"""
__revision__ = '$Id$'
import sys
if sys.version_info[0] == 2 and sys.version_info[1] == 1:
    from Crypto.Util.py21compat import *
from Crypto.Util.py3compat import *
import unittest
from binascii import b2a_hex

class FortunaGeneratorTests(unittest.TestCase):

    def setUp(self):
        global FortunaGenerator
        from Crypto.Random.Fortuna import FortunaGenerator

    def test_generator(self):
        """FortunaGenerator.AESGenerator"""
        fg = FortunaGenerator.AESGenerator()
        self.assertRaises(Exception, fg.pseudo_random_data, 1)
        self.assertEqual(0, fg.counter.next_value())
        fg.reseed(b('Hello'))
        self.assertEqual(b('0ea6919d4361551364242a4ba890f8f073676e82cf1a52bb880f7e496648b565'), b2a_hex(fg.key))
        self.assertEqual(1, fg.counter.next_value())
        self.assertEqual(b('7cbe2c17684ac223d08969ee8b565616') + b('717661c0d2f4758bd6ba140bf3791abd'), b2a_hex(fg.pseudo_random_data(32)))
        self.assertEqual(b('33a1bb21987859caf2bbfc5615bef56d') + b('e6b71ff9f37112d0c193a135160862b7'), b2a_hex(fg.key))
        self.assertEqual(5, fg.counter.next_value())
        self.assertEqual(b('fd6648ba3086e919cee34904ef09a7ff') + b('021f77580558b8c3e9248275f23042bf'), b2a_hex(fg.pseudo_random_data(32)))
        self.assertRaises(AssertionError, fg._pseudo_random_data, 1048577)


def get_tests(config={}):
    from Crypto.SelfTest.st_common import list_test_cases
    return list_test_cases(FortunaGeneratorTests)


if __name__ == '__main__':
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')