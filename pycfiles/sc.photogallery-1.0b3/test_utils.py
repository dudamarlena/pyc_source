# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/sc.photogallery/src/sc/photogallery/tests/test_utils.py
# Compiled at: 2018-01-29 16:00:07
from sc.photogallery.utils import human_readable_size
import unittest

class UtilsTestCase(unittest.TestCase):

    def test_human_readable_size(self):
        with self.assertRaises(ValueError):
            human_readable_size(-5)
        self.assertEqual(human_readable_size(0), '0')
        self.assertEqual(human_readable_size(5), '5')
        self.assertEqual(human_readable_size(5000), '4.9 kB')
        self.assertEqual(human_readable_size(5000000), '4.8 MB')
        self.assertEqual(human_readable_size(5000000000), '4.7 GB')
        self.assertEqual(human_readable_size(5000000000000), '4656.6 GB')