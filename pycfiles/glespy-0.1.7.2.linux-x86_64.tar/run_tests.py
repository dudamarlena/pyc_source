# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/glespy/run_tests.py
# Compiled at: 2013-09-14 06:41:10
__author__ = 'yarnaid'
import unittest, test.test_pixelmap as test_pixelmap, test.test_properties as test_properties, tools.test.test_convertation as test_convertation, tools.test.test_tools as test_tools
loader = unittest.TestLoader()
suite_glespy = loader.loadTestsFromModule(test_pixelmap)
suite_glespy.addTest(loader.loadTestsFromModule(test_properties))
suite_tools = loader.loadTestsFromModule(test_convertation)
suite_tools = loader.loadTestsFromModule(test_tools)
runner = unittest.TextTestRunner()