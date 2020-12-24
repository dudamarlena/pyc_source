# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_24.py
# Compiled at: 2017-12-02 13:53:19
"""
CPython 2.4 bytecode opcodes

This is a like Python 2.3's opcode.py with some classification
of stack usage.
"""
import xdis.opcodes.opcode_2x as opcode_2x
from xdis.opcodes.base import def_op, init_opdata, finalize_opcodes, format_extended_arg, update_pj2
version = 2.4
l = locals()
init_opdata(l, opcode_2x, version)
def_op(l, 'NOP', 9, 0, 0)
def_op(l, 'LIST_APPEND', 18, 2, 1)
def_op(l, 'YIELD_VALUE', 86, 1, 0)
update_pj2(globals(), l)
opcode_arg_fmt = {'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)