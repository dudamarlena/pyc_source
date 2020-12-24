# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py_db_wrapper/exceptions.py
# Compiled at: 2019-04-15 16:23:56
# Size of source mod 2**32: 412 bytes


class TYPE_NOT_DEFINED(Exception):
    __doc__ = 'Raised when the requested data type has not been defined in the library'

    def __init___(self, dErrorArguments):
        Exception.__init__(self, 'exception was raised with arguments {0}'.format(dErrArguments))
        self.dErrorArguments = dErrorArguements


class TABLE_NOT_FOUND(Exception):
    __doc__ = ''


class STATEMENT_EXCEPTION(Exception):
    pass