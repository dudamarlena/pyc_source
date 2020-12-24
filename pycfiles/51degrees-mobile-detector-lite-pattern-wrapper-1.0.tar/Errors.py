# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\TestSuite\Errors.py
# Compiled at: 2002-07-17 17:57:31
__doc__ = '\nExceptions used in TestSuite modules.\n\nCopyright 2002 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
__revision__ = '$Id: Errors.py,v 1.1 2002-07-17 22:57:31 jkloth Exp $'

class TestSuiteError(Exception):
    __module__ = __name__


class TestSuiteSetupError(TestSuiteError):
    __module__ = __name__


class TestSuiteInternalError(TestSuiteError):
    __module__ = __name__


class TestSuiteArgumentError(TestSuiteError):
    __module__ = __name__