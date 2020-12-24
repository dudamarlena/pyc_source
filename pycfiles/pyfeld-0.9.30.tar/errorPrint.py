# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/errorPrint.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import print_function
import sys

def err_print(*args, **kwargs):
    print(file=sys.stderr, *args, **kwargs)