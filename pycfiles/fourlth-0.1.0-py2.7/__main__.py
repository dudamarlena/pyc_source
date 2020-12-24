# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/fourlth/__main__.py
# Compiled at: 2013-07-22 03:18:24
import logging
log = logging.getLogger('fourlth')
import sys, os
from __init__ import *
from loader import *

def main():
    """Simple, interactive interpreter for testing ONLY.
"""
    interp = loader(sys.stdin, prompt_str='> ', interp=None)
    if interp:
        print interp() or ''
    return


if __name__ == '__main__':
    main()