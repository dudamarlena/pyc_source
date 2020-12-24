# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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