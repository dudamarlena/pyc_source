# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/byteop/byteop33.py
# Compiled at: 2020-05-02 10:41:39
"""Byte Interpreter operations for Python 3.3
"""
from __future__ import print_function, division
from xpython.byteop.byteop32 import ByteOp32

class ByteOp33(ByteOp32):

    def __init__(self, vm):
        self.vm = vm
        self.version = 3.3


if __name__ == '__main__':
    x = ByteOp33(None)