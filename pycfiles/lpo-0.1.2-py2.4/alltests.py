# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lpo/test/alltests.py
# Compiled at: 2008-07-30 12:52:46
import testbase, unittest, doctests, testexpression, testexpressionset

def suite():
    alltests = unittest.TestSuite()
    for suite in (doctests, testexpression, testexpressionset):
        alltests.addTest(suite.suite())

    return alltests


if __name__ == '__main__':
    testbase.main(suite())