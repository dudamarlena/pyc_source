# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/paulina/pangtree/tests/datamodel/tests_hello2.py
# Compiled at: 2019-11-19 06:07:04
# Size of source mod 2**32: 289 bytes
import unittest

class Testing(unittest.TestCase):

    def test_string(self):
        a = 'some'
        b = 'some'
        self.assertEqual(a, b)

    def test_boolean(self):
        a = True
        b = True
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()