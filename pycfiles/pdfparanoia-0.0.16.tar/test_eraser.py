# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kanzure/code/pdfparanoia/tests/test_eraser.py
# Compiled at: 2013-07-09 00:34:42
import unittest
from pdfparanoia.eraser import remove_object_by_id

class EraserTestCase(unittest.TestCase):

    def test_remove_object_by_id(self):
        content = ''
        output = remove_object_by_id(content, 1)
        self.assertEqual(content, output)
        content = ''
        output = remove_object_by_id(content, 2)
        self.assertEqual(content, output)
        content = ''
        output = remove_object_by_id(content, 100)
        self.assertEqual(content, output)
        content = '1 0 obj\nthings\nendobj\nleftovers'
        output = remove_object_by_id(content, 2)
        self.assertEqual(content, output)
        content = '1 0 obj\nthings\nendobj\nleftovers'
        output = remove_object_by_id(content, 1)
        self.assertEqual('leftovers', output)