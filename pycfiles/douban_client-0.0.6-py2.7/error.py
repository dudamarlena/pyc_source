# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/douban_client/api/error.py
# Compiled at: 2013-12-18 08:08:21


class DoubanBaseError(Exception):

    def __str__(self):
        return '***%s (%s)*** %s' % (self.status, self.reason, self.msg)


class DoubanOAuthError(DoubanBaseError):

    def __init__(self, status, reason, msg={}):
        self.status = status
        self.reason = reason
        self.msg = {}


class DoubanAPIError(DoubanBaseError):

    def __init__(self, resp):
        self.status = resp.status
        self.reason = resp.reason
        self.msg = resp.parsed