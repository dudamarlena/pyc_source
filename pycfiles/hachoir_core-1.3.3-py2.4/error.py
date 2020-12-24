# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/error.py
# Compiled at: 2010-01-20 17:54:40
"""
Functions to display an error (error, warning or information) message.
"""
from hachoir_core.log import log
from hachoir_core.tools import makePrintable
import sys, traceback

def getBacktrace(empty='Empty backtrace.'):
    """
    Try to get backtrace as string.
    Returns "Error while trying to get backtrace" on failure.
    """
    try:
        info = sys.exc_info()
        trace = traceback.format_exception(*info)
        sys.exc_clear()
        if trace[0] != 'None\n':
            return ('').join(trace)
    except:
        return 'Error while trying to get backtrace'

    return empty


class HachoirError(Exception):
    """
    Parent of all errors in Hachoir library
    """
    __module__ = __name__

    def __init__(self, message):
        message_bytes = makePrintable(message, 'ASCII')
        Exception.__init__(self, message_bytes)
        self.text = message

    def __unicode__(self):
        return self.text


HACHOIR_ERRORS = (
 HachoirError, LookupError, NameError, AttributeError, TypeError, ValueError, ArithmeticError, RuntimeError)
info = log.info
warning = log.warning
error = log.error