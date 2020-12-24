# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/byteop/byteop36pypy.py
# Compiled at: 2020-05-08 04:58:02
"""Bytecode Interpreter operations for PyPy 3.6
"""
from __future__ import print_function, division
from xpython.byteop.byteop36 import ByteOp36
from xpython.byteop.byteoppypy import ByteOpPyPy

class ByteOp36PyPy(ByteOp36, ByteOpPyPy):

    def __init__(self, vm):
        super(ByteOp36PyPy, self).__init__(vm)