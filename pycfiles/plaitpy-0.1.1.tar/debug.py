# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/okay/tonka/src/plait.py/src/debug.py
# Compiled at: 2018-01-25 11:35:46
from __future__ import print_function
from os import environ as ENV
import sys
DEBUG = 'DEBUG' in ENV
VERBOSE = False

def debug(*args):
    if DEBUG:
        print((' ').join(map(str, args)), file=sys.stderr)


def verbose(*args):
    if VERBOSE:
        print((' ').join(map(str, args)), file=sys.stderr)