# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukasz/develop/workspace/monolith/build/lib/monolith/cli/exceptions.py
# Compiled at: 2013-11-25 17:19:09
# Size of source mod 2**32: 263 bytes


class MonolithError(Exception):

    def __init__(self, message, code=-1):
        self.message = message
        self.code = code


class CLIError(MonolithError):
    pass


class CommandError(CLIError):
    pass


class AlreadyRegistered(CLIError):
    pass