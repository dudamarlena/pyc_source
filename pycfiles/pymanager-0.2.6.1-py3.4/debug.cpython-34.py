# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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