# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pymutils/debug.py
# Compiled at: 2015-04-29 09:22:29
# Size of source mod 2**32: 496 bytes
from .global_storage import Globals
import sys

def tofileln(message):
    if Globals.outfile is None:
        Globals.outfile = sys.stdout
    if Globals.outfile is sys.stdout:
        print(message, file=sys.stdout)
    else:
        b = '{0}\n'.format(message).encode('utf-8')
        Globals.outfile.write(b)


def debug(message):
    if Globals.verbose >= 2:
        tofileln('[DEBUG] {0}'.format(message))


def verbose(message):
    if Globals.verbose >= 1:
        tofileln('[INFO] {0}'.format(message))


def log(message):
    tofileln(message)