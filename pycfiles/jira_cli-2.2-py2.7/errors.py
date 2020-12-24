# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/jiracli/errors.py
# Compiled at: 2016-10-11 22:05:56
try:
    from jira.utils import JIRAError
except:
    from jira.exceptions import JIRAError

from suds import WebFault

class JiraInitializationError(Exception):
    pass


class JiraAuthenticationError(Exception):
    pass


class UsageError(Exception):
    pass


class UsageWarning(Exception):
    pass


class JiraCliError(Exception):

    def __init__(self, exc):
        if isinstance(exc, WebFault):
            msg = (':').join(exc.fault.faultstring.split(':')[1:]).strip()
            super(JiraCliError, self).__init__(msg)
        elif isinstance(exc, JIRAError):
            if exc.status_code == 401:
                super(JiraCliError, self).__init__('invalid username/password')
            else:
                super(JiraCliError, self).__init__(exc.text)
        else:
            super(JiraCliError, self).__init__(exc)