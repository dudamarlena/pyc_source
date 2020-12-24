# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/byteop/byteop26.py
# Compiled at: 2020-05-02 07:39:26
"""Bytecode Interpreter operations for Python 2.6
"""
from __future__ import print_function, division
from xpython.byteop.byteop25 import ByteOp25

class ByteOp26(ByteOp25):

    def __init__(self, vm):
        self.vm = vm
        self.version = 2.6