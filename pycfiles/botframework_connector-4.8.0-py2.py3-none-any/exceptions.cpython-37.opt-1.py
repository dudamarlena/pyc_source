# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /botfly/exceptions.py
# Compiled at: 2019-10-27 23:53:09
# Size of source mod 2**32: 1173 bytes
__doc__ = '\nCommon exceptions.\n'

class CLIException(Exception):

    def __init__(self, value=None):
        self.value = value


class CommandQuit(CLIException):
    """CommandQuit"""
    pass


class CommandExit(CLIException):
    """CommandExit"""
    pass


class NewCommand(CLIException):
    """NewCommand"""
    pass