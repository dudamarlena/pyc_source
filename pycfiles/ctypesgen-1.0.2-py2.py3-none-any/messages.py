# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/messages.py
# Compiled at: 2019-08-18 21:39:19
"""
ctypesgen.messages contains functions to display status, error, or warning
messages to the user. Warning and error messages are also associated
with a "message class", which is a string, which currently has no effect.

Error classes are:
'usage' - there was something funny about the command-line parameters
'cparser' - there was a syntax error in the header file
'missing-library' - a library could not be loaded
'macro' - a macro could not be translated to Python
'unsupported-type' - there was a type in the header that ctypes cannot use, like
    "long double".
'other' - catchall.

Warning classes are:
'usage' - there was something funny about the command-line parameters
'rename' - a description has been renamed to avoid a name conflict
'other' - catchall.
"""
import sys, logging
__all__ = [
 'error_message', 'warning_message', 'status_message']
log = logging.getLogger('ctypesgen')
ch = logging.StreamHandler()
logging_fmt_str = '%(levelname)s: %(message)s'
formatter = logging.Formatter(logging_fmt_str)
ch.setFormatter(formatter)
log.addHandler(ch)
log.setLevel(logging.INFO)

def error_message(msg, cls=None):
    log.error('%s', msg)


def warning_message(msg, cls=None):
    log.warning('%s', msg)


def status_message(msg):
    log.info('Status: %s', msg)