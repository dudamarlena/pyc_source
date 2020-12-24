# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/imagehash/tests/test_old_hex_conversions.py
# Compiled at: 2017-12-06 18:12:41
import unittest, numpy as np, imagehash
old_hexadecimal_to_bool_array = [
 [
  'ffeb89818193ffff',
  np.array([[True, True, True, True, True, True, True, True],
   [
    True, True, False, True, False, True, True, True],
   [
    True, False, False, True, False, False, False, True],
   [
    True, False, False, False, False, False, False, True],
   [
    True, False, False, False, False, False, False, True],
   [
    True, True, False, False, True, False, False, True],
   [
    True, True, True, True, True, True, True, True],
   [
    True, True, True, True, True, True, True, True]])]]

class TestOldHexConversions(unittest.TestCase):

    def setUp(self):
        self.from_hex = imagehash.old_hex_to_hash

    def test_hex_to_hash_output(self):
        for case in old_hexadecimal_to_bool_array:
            self.assertTrue(np.array_equal(case[1], self.from_hex(case[0]).hash))


if __name__ == '__main__':
    unittest.main()