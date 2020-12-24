# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/byteop/byteop27pypy.py
# Compiled at: 2020-05-08 05:03:41
"""Bytecode Interpreter operations for PyPy Python 2.7
"""
from __future__ import print_function, division
from xpython.byteop.byteop27 import ByteOp27
from xpython.byteop.byteoppypy import ByteOpPyPy

class ByteOp27PyPy(ByteOp27, ByteOpPyPy):

    def __init__(self, vm):
        super(ByteOp27PyPy, self).__init__(vm)