# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/harold/tests/files_three/nopackage.py
# Compiled at: 2006-08-02 05:57:50
import socket, random

def get():
    return 'callables within modules (but not packages work), too'


get.expose = True