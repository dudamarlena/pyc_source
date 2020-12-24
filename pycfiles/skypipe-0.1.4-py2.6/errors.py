# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/dotcloud/client/errors.py
# Compiled at: 2012-09-19 14:56:08


class RESTAPIError(Exception):

    def __init__(self, code=None, desc=None, trace_id=None):
        self.code = code
        self.desc = desc
        self.trace_id = trace_id

    def __str__(self):
        return self.desc


class AuthenticationNotConfigured(Exception):
    pass