# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/qcrash/qcrash/formatters/markdown.py
# Compiled at: 2016-12-29 05:40:24
# Size of source mod 2**32: 1266 bytes
"""
A PyQt/PySide framework for reporting application crash (unhandled exception)
and let the user report an issue/feature request.
"""
from .base import BaseFormatter
BODY_ITEM_TEMPLATE = '### %(name)s\n\n%(value)s\n\n'
NB_LINES_MAX = 50

class MardownFormatter(BaseFormatter):
    __doc__ = '\n    Formats the issue report using Markdown.\n    '

    def format_body(self, description, sys_info=None, traceback=None):
        """
        Formats the body using markdown.

        :param description: Description of the issue, written by the user.
        :param sys_info: Optional system information string
        :param log: Optional application log
        :param traceback: Optional traceback.
        """
        body = BODY_ITEM_TEMPLATE % {'name': 'Description', 'value': description}
        if traceback:
            traceback = '\n'.join(traceback.splitlines()[-NB_LINES_MAX:])
            body += BODY_ITEM_TEMPLATE % {'name': 'Traceback', 'value': '```\n%s\n```' % traceback}
        if sys_info:
            sys_info = '- %s' % '\n- '.join(sys_info.splitlines())
            body += BODY_ITEM_TEMPLATE % {'name': 'System information', 'value': sys_info}
        return body