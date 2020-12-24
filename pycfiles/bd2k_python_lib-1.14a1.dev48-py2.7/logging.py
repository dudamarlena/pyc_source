# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bd2k/util/logging.py
# Compiled at: 2018-05-03 13:55:55
from __future__ import absolute_import
import codecs, types, logging

class Utf8SyslogFormatter(logging.Formatter):
    """
    Works around http://bugs.python.org/issue14452
    """

    def format(self, record):
        origGetMessage = record.getMessage

        def getMessage(_self):
            msg = origGetMessage()
            if isinstance(msg, str):
                try:
                    msg = msg.encode('ascii')
                except UnicodeEncodeError:
                    msg = codecs.BOM + msg.encode('utf8')

            return msg

        types.MethodType(getMessage, record, logging.LogRecord)
        record.getMessage = types.MethodType(getMessage, record, logging.LogRecord)
        return logging.Formatter.format(self, record)