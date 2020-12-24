# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/log/formatter.py
# Compiled at: 2015-11-06 23:45:35
import logging
from salve.context import ExecutionContext
try:
    unicode
except NameError:
    unicode = str

class Formatter(logging.Formatter):
    """
    Log message formatter.
    """

    def format(self, record):
        """
        Format records according to time, current exec context, log level, and
        their message contents.

        Args:
            @record
            The LogRecord object whose attributes will be fed to the logging.
        """

        def bracket(s):
            return '[' + s + ']'

        if not hasattr(record, 'hide_salve_context'):
            record.hide_salve_context = None
        out_arr = []
        if not record.hide_salve_context:
            out_arr.append(unicode(ExecutionContext()))
        out_arr.append(bracket(record.levelname))
        out_arr.append(record.msg % record.args)
        return (' ').join(out_arr)