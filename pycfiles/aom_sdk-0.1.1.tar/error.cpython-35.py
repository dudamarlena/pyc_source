# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aomi/error.py
# Compiled at: 2017-11-17 12:53:02
# Size of source mod 2**32: 940 bytes
__doc__ = ' Slightly less terrible error handling and reporting '
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