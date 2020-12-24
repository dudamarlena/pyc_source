# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/builder/builder_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 779 bytes
import time, unittest
from bibliopixel.builder.builder import Builder
from bibliopixel.util import data_file

class BuilderTest(unittest.TestCase):

    def test_simple(self):
        b = Builder(driver='dummy')
        self.assertFalse(b.is_running)
        b.start(True)
        self.assertTrue(b.is_running)
        b.stop()

    def test_merging(self):
        b = Builder(driver='.dummy') + {'animation': '.tests.PixelTester'}
        b.desc.shape = [12, 16]
        b.start(True)
        actual = b.desc.as_dict()
        b.stop()
        expected = {'animation':{'typename': '.tests.PixelTester'}, 
         'driver':{'typename': '.dummy'}, 
         'run':{'threaded': True}, 
         'shape':[
          12, 16]}
        self.assertEqual(actual, expected)