# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/tests/files_three/nopackage.py
# Compiled at: 2006-08-02 05:57:50
import socket, random

def get():
    return 'callables within modules (but not packages work), too'


get.expose = True