# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/shanedasilva/src/ghc/coinbase/coinbase-python/tests/test_util.py
# Compiled at: 2018-01-17 19:23:46
# Size of source mod 2**32: 1206 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import unittest2
from coinbase.wallet.util import clean_params

class TestUtils(unittest2.TestCase):

    def test_clean_params(self):
        input = {'none':None, 
         'int':1, 
         'float':2.0, 
         'bool':True, 
         'nested':{'none':None, 
          'int':1, 
          'float':2.0, 
          'bool':False}}
        self.assertEqual(clean_params(input), {'int':1, 
         'float':2.0, 
         'bool':True, 
         'nested':{'int':1, 
          'float':2.0, 
          'bool':False}})
        self.assertEqual(clean_params(input, drop_nones=False), {'none':None, 
         'int':1, 
         'float':2.0, 
         'bool':1, 
         'nested':{'none':None, 
          'int':1, 
          'float':2.0, 
          'bool':0}})
        self.assertEqual(clean_params(input, recursive=False), {'int':1, 
         'float':2.0, 
         'bool':1, 
         'nested':{'none':None, 
          'int':1, 
          'float':2.0, 
          'bool':0}})