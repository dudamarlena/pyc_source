# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treedraw/util.py
# Compiled at: 2017-10-18 02:00:45
# Size of source mod 2**32: 137 bytes
import sys

def warning(string):
    print(' :: warning:', string)


def error(string):
    print(' :: error:  ', string)
    sys.exit(0)