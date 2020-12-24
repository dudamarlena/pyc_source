# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/urltest/tests/generators.py
# Compiled at: 2009-07-01 11:18:15
"""These tests check the test generator in urltest"""
import unittest
from urltest import test_generator

class GeneratorTests(unittest.TestCase):

    def test_method_generator_returns_callable(self):
        item = {'url': '/', 'code': 200}
        test_method = test_generator(item)
        assert hasattr(test_method, '__call__')


if __name__ == '__main__':
    unittest.main()