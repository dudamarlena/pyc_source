# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ao/tron/tests.py
# Compiled at: 2010-03-20 22:57:16
import doctest, unittest
docfiles = [
 'input.txt',
 'board.txt']

def test_suite():
    """This is the test siute we use to run tests."""
    tests = [ doctest.DocFileSuite(file, optionflags=doctest.ELLIPSIS) for file in docfiles
            ]
    return unittest.TestSuite(tests)