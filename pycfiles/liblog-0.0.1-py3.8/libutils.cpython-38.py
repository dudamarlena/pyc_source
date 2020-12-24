# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/libutils/libutils.py
# Compiled at: 2020-04-28 06:46:42
# Size of source mod 2**32: 118 bytes
import os, sys

def real_path(filename):
    return os.path.dirname(os.path.abspath(sys.argv[0])) + f"/{filename}"