# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/exceptions.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 1045 bytes
from cashew.exceptions import InactivePlugin
from cashew.exceptions import UserFeedback
from dexy.version import DEXY_VERSION
import dexy.utils, platform

class NoFilterOutput(UserFeedback):
    pass


class CircularDependency(UserFeedback):
    pass


class BlankAlias(UserFeedback):
    pass


class InvalidStateTransition(Exception):
    pass


class UnexpectedState(Exception):
    pass


class InternalDexyProblem(Exception):

    def __init__(self, message):
        self.message = dexy.utils.s('\n        Oops! You may have found a bug in Dexy.\n        The developer would really appreciate if you copy and paste this entire message\n        and the Traceback above it into an email and send to info@dexy.it\n        Your version of Dexy is %s\n        Your platform is %s' % (DEXY_VERSION, platform.system()))
        self.message += '\n'
        self.message += message

    def __str__(self):
        return self.message


class DeprecatedException(InternalDexyProblem):
    pass


class TemplateException(InternalDexyProblem):
    pass