# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pyfeld/errorPrint.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import print_function
import sys

def err_print(*args, **kwargs):
    print(file=sys.stderr, *args, **kwargs)