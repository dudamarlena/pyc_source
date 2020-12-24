# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/qcrash/qcrash/formatters/email.py
# Compiled at: 2016-12-29 05:40:24
# Size of source mod 2**32: 1785 bytes
"""
This module contains the Html formatter used by the email backend.
"""
from .base import BaseFormatter
BODY_ITEM_TEMPLATE = '%(name)s\n%(delim)s\n\n%(value)s\n\n\n'
NB_LINES_MAX = 50

class EmailFormatter(BaseFormatter):
    __doc__ = '\n    Formats the crash report for use in an email (text/plain)\n    '

    def __init__(self, app_name=None):
        """
        :param app_name: Name of the application. If set the email subject will
             starts with [app_name]
        """
        self.app_name = app_name

    def format_title(self, title):
        """
        Formats title (add ``[app_name]`` if app_name is not None).
        """
        if self.app_name:
            return '[%s] %s' % (self.app_name, title)
        return title

    def format_body(self, description, sys_info=None, traceback=None):
        """
        Formats the body in plain text. (add a series of '-' under each section
            title).

        :param description: Description of the issue, written by the user.
        :param sys_info: Optional system information string
        :param log: Optional application log
        :param traceback: Optional traceback.
        """
        name = 'Description'
        delim = '-' * 40
        body = BODY_ITEM_TEMPLATE % {'name': name, 'value': description, 'delim': delim}
        if traceback:
            name = 'Traceback'
            traceback = '\n'.join(traceback.splitlines()[-NB_LINES_MAX:])
            body += BODY_ITEM_TEMPLATE % {'name': name, 'value': traceback, 'delim': delim}
        if sys_info:
            name = 'System information'
            body += BODY_ITEM_TEMPLATE % {'name': name, 'value': sys_info, 'delim': delim}
        return body