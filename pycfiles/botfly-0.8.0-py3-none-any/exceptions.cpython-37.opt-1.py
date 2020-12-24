# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /botfly/exceptions.py
# Compiled at: 2019-10-27 23:53:09
# Size of source mod 2**32: 1173 bytes
"""
Common exceptions.
"""

class CLIException(Exception):

    def __init__(self, value=None):
        self.value = value


class CommandQuit(CLIException):
    __doc__ = 'An exception that is used to signal quiting from a command object.\n    '


class CommandExit(CLIException):
    __doc__ = 'An exception that is used to signal exiting from the command object. The\n    command is not popped.\n    '


class NewCommand(CLIException):
    __doc__ = 'Used to signal the parser to push a new command object.\n    Raise this with an instance of BaseCommands as a value.\n    '