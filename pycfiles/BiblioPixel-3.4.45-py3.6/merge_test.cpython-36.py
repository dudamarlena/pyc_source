# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/project/merge_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1628 bytes
import unittest
from bibliopixel.project import merge
BASE = dict((merge.DEFAULT_PROJECT),
  maker={'typename': 'bibliopixel.project.data_maker.Maker'},
  run={})

class MergeTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(merge.merge(), {})

    def test_single(self):
        self.assertEqual(merge.merge(merge.DEFAULT_PROJECT), BASE)

    def test_more(self):
        result = merge.merge(merge.DEFAULT_PROJECT, {'animation':'foo', 
         'driver':'bar', 
         'drivers':[
          'bang', 'bop']}, {'animation':'bfoo', 
         'maker':{'numpy_dtype': 'float'}, 
         'path':'path/to/dir'}, {'drivers':None, 
         'animation':{'bar':'baz', 
          'bing':'bop'}}, {'animation': {'bing': None}})
        expected = {'aliases':{},  'animation':{'typename':'bfoo', 
          'bar':'baz'}, 
         'controls':[],  'shape':(),  'driver':{'typename': 'bar'}, 
         'drivers':[],  'layout':{},  'numbers':'', 
         'maker':{'numpy_dtype':'float', 
          'typename':'bibliopixel.project.data_maker.Maker'}, 
         'colors':{},  'palettes':{},  'path':'path/to/dir', 
         'run':{},  'typename':'bibliopixel.project.project.Project'}
        self.assertEqual(result, expected)