# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/messages.py
# Compiled at: 2019-08-18 21:39:19
# Size of source mod 2**32: 1385 bytes
__doc__ = '\nctypesgen.messages contains functions to display status, error, or warning\nmessages to the user. Warning and error messages are also associated\nwith a "message class", which is a string, which currently has no effect.\n\nError classes are:\n\'usage\' - there was something funny about the command-line parameters\n\'cparser\' - there was a syntax error in the header file\n\'missing-library\' - a library could not be loaded\n\'macro\' - a macro could not be translated to Python\n\'unsupported-type\' - there was a type in the header that ctypes cannot use, like\n    "long double".\n\'other\' - catchall.\n\nWarning classes are:\n\'usage\' - there was something funny about the command-line parameters\n\'rename\' - a description has been renamed to avoid a name conflict\n\'other\' - catchall.\n'
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