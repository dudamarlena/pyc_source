# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/climb/exceptions.py
# Compiled at: 2015-05-23 15:38:13
# Size of source mod 2**32: 179 bytes


class ConfigNotFound(Exception):
    pass


class CLIException(Exception):
    pass


class UnknownCommand(CLIException):
    pass


class MissingArgument(CLIException):
    pass