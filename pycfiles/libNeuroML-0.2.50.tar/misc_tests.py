# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/padraig/libNeuroML/neuroml/test/misc_tests.py
# Compiled at: 2017-07-07 13:05:49
"""
Miscelaneous unit tests

"""
import sys, inspect, neuroml
try:
    import unittest2 as unittest
except ImportError:
    import unittest

class TestCommonProperties(unittest.TestCase):

    def test_instatiation(self):
        """
        Since classes are auto-generated, need to test that they correctly instantiate
        """
        for name, test_class in inspect.getmembers(sys.modules[neuroml.__name__]):
            if sys.version_info >= (2, 7):
                print sys.version_info
                if inspect.isclass(test_class):
                    ob = test_class()
                    self.assertIsInstance(ob, test_class)
            else:
                print 'Warning - Python<2.7 does not support this test'