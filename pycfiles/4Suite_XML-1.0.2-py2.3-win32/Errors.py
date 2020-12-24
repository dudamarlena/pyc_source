# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\TestSuite\Errors.py
# Compiled at: 2002-07-17 17:57:31
"""
Exceptions used in TestSuite modules.

Copyright 2002 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
__revision__ = '$Id: Errors.py,v 1.1 2002-07-17 22:57:31 jkloth Exp $'

class TestSuiteError(Exception):
    __module__ = __name__


class TestSuiteSetupError(TestSuiteError):
    __module__ = __name__


class TestSuiteInternalError(TestSuiteError):
    __module__ = __name__


class TestSuiteArgumentError(TestSuiteError):
    __module__ = __name__