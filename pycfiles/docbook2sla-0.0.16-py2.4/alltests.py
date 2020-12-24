# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/docbook2sla/tests/alltests.py
# Compiled at: 2008-04-01 13:57:01
import unittest

def suite():
    modules_to_test = ('test_docbook2pageobject', 'test_wrapper', 'test_syncronize',
                       'test_create', 'test_transformation', 'test_image')
    alltests = unittest.TestSuite()
    for module in map(__import__, modules_to_test):
        alltests.addTest(unittest.findTestCases(module))

    return alltests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')