# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deforest/tests/test_ignore_cleaner.py
# Compiled at: 2020-03-13 12:20:39
# Size of source mod 2**32: 1031 bytes
import unittest
import deforest.cleaners as cleaner

class TestIgnoreCleaner(unittest.TestCase):

    def test_clean_no_ignore(self):
        data = {'info':{'title': 'hello world'}, 
         'paths':{'/validations': {'post': {'x-amazon-apigateway-request-validator': 'all'}}}}
        self.result = [
         data]
        sut = cleaner.IgnoreCleaner(self)
        sut.clean()
        assert len(self.result) == 1
        assert self.result[0] == data

    def test_clean_with_ignore(self):
        data = {'info':{'title': 'hello world'}, 
         'paths':{'/validations': {'post':{'x-amazon-apigateway-request-validator':'all',  'x-deforest-ignore':True},  'get':{'parameters': 'something'}}}}
        expected = {'info':{'title': 'hello world'}, 
         'paths':{'/validations': {'get': {'parameters': 'something'}}}}
        self.result = [
         data]
        sut = cleaner.IgnoreCleaner(self)
        sut.clean()
        assert len(self.result) == 1
        assert self.result[0] == expected