# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/gszathmari/munchkin/munchkin/core/utils.py
# Compiled at: 2016-05-02 03:44:35
import sys

def supported_python_version():
    python_version = sys.version.split()[0]
    if python_version >= '3' or python_version < '2.6':
        return False
    return True