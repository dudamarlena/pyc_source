# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aomi/error.py
# Compiled at: 2017-11-17 12:53:02
# Size of source mod 2**32: 940 bytes
""" Slightly less terrible error handling and reporting """
from __future__ import print_function
import sys, traceback

def unhandled(exception, opt):
    """ Handle uncaught/unexpected errors and be polite about it"""
    exmod = type(exception).__module__
    name = '%s.%s' % (exmod, type(exception).__name__)
    if exmod == 'aomi.exceptions' or exmod == 'cryptorito':
        if hasattr(exception, 'source'):
            output(exception.message, opt, extra=exception.source)
        else:
            output(exception.message, opt)
    else:
        output('Unexpected error: %s' % name, opt)
    sys.exit(1)


def output(message, opt, extra=None):
    """ Politely display an unexpected error"""
    print(message, file=sys.stderr)
    if opt.verbose:
        if extra:
            print(extra)
        traceback.print_exc(sys.stderr)