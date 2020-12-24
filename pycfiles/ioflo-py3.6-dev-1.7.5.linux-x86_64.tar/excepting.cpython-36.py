# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/excepting.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 4382 bytes
"""excepting.py exception classes

"""
import random
from ..aid.sixing import *

class ParameterError(Exception):
    __doc__ = 'Used to indicate a function parameter is either of the wrong type or value\n       usage:\n       raise excepting.ParameterError("Expected Frame instance", "active", active)\n    '

    def __init__(self, message=None, name=None, value=None):
        self.message = message
        self.name = name
        self.value = value
        self.args = (
         message, name, value)

    def __str__(self):
        return '%s. Name = %s, Type = %s, Value = %s.\n' % (
         self.message, self.name, str(type(self.value)), repr(self.value))


class ParseError(Exception):
    __doc__ = 'Used to indicate a mission script statement has a parsing error\n\n       usage:\n       msg = "ParseError: Not enough tokens in command \'%s\'" % (kind)\n       raise excepting.ParseError(msg, tokens, index)\n    '

    def __init__(self, message=None, tokens=None, index=None):
        self.message = message
        self.tokens = tokens
        self.index = index
        self.args = (
         message, tokens, index)

    def __str__(self):
        return '%s. tokens = %s, index = %s.\n' % (
         self.message, repr(self.tokens), self.index)


class ParseWarning(Exception):
    __doc__ = 'Used to indicate a mission script statement has a parsing warning\n\n       usage:\n       msg = "ParseWarning: Not enough tokens in command \'%s\'" % (kind)\n       raise excepting.ParseWarning(msg, index, tokens)\n    '

    def __init__(self, message=None, tokens=None, index=None):
        self.message = message
        self.tokens = tokens
        self.index = index
        self.args = (
         message, tokens, index)

    def __str__(self):
        return '%s. tokens = %s  index = %s.\n' % (
         self.message, repr(self.tokens), self.index)


class ResolveError(Exception):
    __doc__ = 'Used to indicate a mission script statement link or reference in an\n       component (framer, frame, action etc) is in error\n\n       usage:\n       msg = "ResolveError: Bad frame link \'%s\' for action \'%s\'" % (link, action.name)\n       raise excepting.ResolveError(msg, link, action)\n    '

    def __init__(self, message=None, name=None, value=None, human='', count=None):
        self.message = message
        self.name = name
        self.value = value
        self.human = human
        self.count = count
        self.args = (
         message, name, value, human, count)

    def __str__(self):
        return '%s. Name = %s, Value = %s. at line %s\n    %s\n' % (
         self.message, self.name, repr(self.value), self.count, self.human)


class CloneError(Exception):
    __doc__ = 'Used to indicate cloning error\n\n       usage:\n       msg = "CloneError: Framer \'%s\' already exists" % (name)\n       raise excepting.CloneError(msg)\n    '

    def __init__(self, message=None):
        self.message = message
        self.args = message

    def __str__(self):
        return '%s.\n' % (self.message,)


class RegisterError(Exception):
    __doc__ = 'Used to indicate error in Registry\n\n       usage:\n       msg = "Entry \'{0}\' already exists in registry".format(rname)\n       raise excepting.RegisterError(msg)\n    '

    def __init__(self, message=None):
        self.message = message
        self.args = message

    def __str__(self):
        return '{0}: {1}.\n'.format(self.__class__.__name__, self.message)


class TimerRetroError(Exception):
    __doc__ = 'Used to indicate timer base has retrograded while timer is running\n\n       usage:\n\n       raise excepting.TimerRetrogradeError(msg)\n    '

    def __init__(self, message=None):
        self.message = message
        self.args = message

    def __str__(self):
        return '{0}: {1}.\n'.format(self.__class__.__name__, self.message)


def Test():
    """Module self test

    """
    raise ParameterError('Expected something else', 'whatever', 1)


if __name__ == '__main__':
    Test()