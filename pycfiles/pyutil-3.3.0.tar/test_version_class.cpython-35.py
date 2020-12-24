# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/test_version_class.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 996 bytes
import unittest
from pyutil import version_class
V = version_class.Version

class T(unittest.TestCase):

    def test_rc_regex_rejects_rc_suffix(self):
        self.assertRaises(ValueError, V, '9.9.9rc9')

    def test_rc_regex_rejects_trailing_garbage(self):
        self.assertRaises(ValueError, V, '9.9.9c9HEYTHISISNTRIGHT')

    def test_comparisons(self):
        self.assertTrue(V('1.0') < V('1.1'))
        self.assertTrue(V('1.0a1') < V('1.0'))
        self.assertTrue(V('1.0a1') < V('1.0b1'))
        self.assertTrue(V('1.0b1') < V('1.0c1'))
        self.assertTrue(V('1.0a1') < V('1.0a1-r99'))
        self.assertEqual(V('1.0a1.post987'), V('1.0a1-r987'))
        self.assertEqual(str(V('1.0a1.post999')), '1.0.0a1-r999')
        self.assertEqual(str(V('1.0a1-r999')), '1.0.0a1-r999')
        self.assertNotEqual(V('1.0a1'), V('1.0a1-r987'))