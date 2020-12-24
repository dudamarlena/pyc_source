# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/indra/base/tests/testDocTests.py
# Compiled at: 2008-07-21 18:55:14
import unittest, doctest
optionflags = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocFileSuite('indrabase.txt', package='indra.base.tests'))
    return suite