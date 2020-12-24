# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/byteop/byteop32pypy.py
# Compiled at: 2020-05-08 04:59:06
"""Bytecode Interpreter operations for PyPy 3.2
"""
from __future__ import print_function, division
from xpython.byteop.byteop32 import ByteOp32
from xpython.byteop.byteoppypy import ByteOpPyPy

class ByteOp32PyPy(ByteOp32, ByteOpPyPy):

    def __init__(self, vm):
        super(ByteOp32PyPy, self).__init__(vm)