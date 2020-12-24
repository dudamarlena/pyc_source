# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/bliptv/reader/tests.py
# Compiled at: 2008-07-27 06:26:37
import unittest, doctest
optionflags = doctest.ELLIPSIS

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocFileSuite('README.txt', package='bliptv.reader', optionflags=optionflags))
    return suite