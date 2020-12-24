# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kentcoble/Documents/workspace/easysnmp/easysnmp/compat.py
# Compiled at: 2016-04-23 17:04:30
import logging, sys
PY3 = sys.version_info[0] == 3
if PY3:
    text_type = str

    def ub(s):
        return s


    def urepr(s):
        return repr(s)


else:
    text_type = unicode

    def ub(s):
        return s.decode('latin-1')


    def urepr(s):
        if isinstance(s, unicode):
            return repr(s)[1:]
        else:
            return repr(s)


class NullHandler(logging.Handler):
    """
    This handler does nothing. It's intended to be used to avoid the
    "No handlers could be found for logger XXX" one-off warning.
    """

    def handle(self, record):
        pass

    def emit(self, record):
        pass

    def createLock(self):
        self.lock = None
        return