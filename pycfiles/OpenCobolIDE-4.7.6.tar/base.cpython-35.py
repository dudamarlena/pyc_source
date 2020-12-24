# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/qcrash/qcrash/formatters/base.py
# Compiled at: 2016-12-29 05:40:24
# Size of source mod 2**32: 819 bytes


class BaseFormatter(object):
    __doc__ = '\n    Base class for implementing a custom formatter.\n\n    Just implement :meth:`format_body` and :meth:`format_title` functions and\n    set your formatter on the backends you created.\n    '

    def format_title(self, title):
        """
        Formats the issue title. By default this method does nothing.

        An email formatter might want to append the application to name to
        the object field...
        """
        return title

    def format_body(self, description, sys_info=None, traceback=None):
        """
        Not implemented.

        :param description: Description of the issue, written by the user.
        :param sys_info: Optional system information string
        :param traceback: Optional traceback.
        """
        raise NotImplementedError