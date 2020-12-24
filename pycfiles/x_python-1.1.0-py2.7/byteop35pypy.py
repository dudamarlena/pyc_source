# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/byteop/byteop35pypy.py
# Compiled at: 2020-05-08 05:06:27
"""Bytecode Interpreter operations for PyPy 3.5
"""
from __future__ import print_function, division
from xpython.byteop.byteop35 import ByteOp35
from xpython.byteop.byteoppypy import ByteOpPyPy

class ByteOp35PyPy(ByteOp35, ByteOpPyPy):

    def __init__(self, vm):
        super(ByteOp35PyPy, self).__init__(vm)