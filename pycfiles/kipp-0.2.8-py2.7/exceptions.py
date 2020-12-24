# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/kipp/runner/exceptions.py
# Compiled at: 2017-11-06 03:31:03
from __future__ import unicode_literals
from kipp.libs import KippException

class KippRunnerException(KippException):
    pass


class KippRunnerTimeoutException(KippRunnerException):
    pass


class KippRunnerSIGTERMException(KippRunnerException):
    pass