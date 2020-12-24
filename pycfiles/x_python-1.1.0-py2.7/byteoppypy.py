# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/byteop/byteoppypy.py
# Compiled at: 2020-05-08 04:15:51
"""Bytecode Interpreter operations for PyPy in general (all versions)

Specific PyPy versions i.e. PyPy 2.7, 3.2, 3.5, and 3.6 inherit this.
"""
from __future__ import print_function, division

class ByteOpPyPy(object):

    def LOOKUP_METHOD(self, count):
        """
        """
        raise self.vm.VMError('LOOKUP_METHOD not implemented yet')

    def CALL_METHOD(self, count):
        """
        """
        raise self.vm.VMError('CALL_METHOD not implemented yet')