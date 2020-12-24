# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/profpy/apis/utils/exceptions.py
# Compiled at: 2020-01-07 15:07:46
# Size of source mod 2**32: 353 bytes


class ParameterException(Exception):

    def __init__(self, message):
        super(ParameterException, self).__init__(message)


class ApiException(Exception):
    __doc__ = '\n    General API-related exceptions\n    '

    def __init__(self, message, error_code=None):
        super(ApiException, self).__init__(message)
        self.status_code = error_code