# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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