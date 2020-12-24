# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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