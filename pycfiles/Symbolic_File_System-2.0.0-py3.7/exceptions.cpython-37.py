# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sfs/exceptions.py
# Compiled at: 2018-12-21 03:03:15
# Size of source mod 2**32: 211 bytes


class SFSException(Exception):
    __doc__ = 'Base Class for all SFS related exceptions'


class CLIValidationException(SFSException):
    __doc__ = 'Exception class for validation errors in CLI commands'