# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deforest/tests/test_default_cleaner.py
# Compiled at: 2020-03-13 12:20:39
# Size of source mod 2**32: 743 bytes
import unittest
import deforest.cleaners as cleaner

class TestIgnoreCleaner(unittest.TestCase):

    def test_clean_(self):
        data = {'info':{'title': 'hello world'}, 
         'paths':{'/validations': {'post':{'x-amazon-apigateway-request-validator':'all',  'x-deforest-ignore':True},  'get':{'parameters':'something',  'x-amazon-something':{'this': 'is a child'}}}}}
        expected = {'info':{'title': 'hello world'}, 
         'paths':{'/validations': {'post':{'x-deforest-ignore': True},  'get':{'parameters': 'something'}}}}
        self.result = [
         data]
        sut = cleaner.DefaultCleaner(self)
        sut.clean()
        assert len(self.result) == 1
        assert self.result[0] == expected