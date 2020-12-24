# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/services/exception.py
# Compiled at: 2012-10-12 07:02:39
import sys
from coils.core import CoilsException

class BPMException(CoilsException):

    def error_code(self):
        return 500

    def __str__(self):
        return self.text


class NoActionException(BPMException):

    def error_code(self):
        return 500

    def __str__(self):
        return self.text


class UnknownActionException(BPMException):

    def error_code(self):
        return 500

    def __str__(self):
        return self.text


class NoSuchMessageException(BPMException):

    def error_code(self):
        return 500

    def __str__(self):
        return self.text