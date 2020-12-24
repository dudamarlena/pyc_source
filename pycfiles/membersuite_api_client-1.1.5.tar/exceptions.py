# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/var/pyenv/versions/hub/lib/python2.7/site-packages/membersuite_api_client/exceptions.py
# Compiled at: 2018-06-12 17:42:21
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import python_2_unicode_compatible

@python_2_unicode_compatible
class MemberSuiteAPIError(Exception):

    def __init__(self, result):
        self.result = result
        self.exception_type = self.__class__.__name__

    def __str__(self):
        concierge_error = self.get_concierge_error()
        return (b'<{exception_type} ConciergeError: {concierge_error}>').format(exception_type=self.exception_type, concierge_error=concierge_error)

    def get_concierge_error(self):
        try:
            return self.result[b'body'][self.result_type][b'Errors'][b'ConciergeError']
        except KeyError:
            return self.result[b'Errors']


class LoginToPortalError(MemberSuiteAPIError):
    pass


class LogoutError(MemberSuiteAPIError):
    pass


class ExecuteMSQLError(MemberSuiteAPIError):
    pass


class NoResultsError(MemberSuiteAPIError):
    pass


class NotAnObjectQuery(MemberSuiteAPIError):
    pass