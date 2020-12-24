# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_30.py
# Compiled at: 2020-04-26 21:30:10
"""
CPython 3.0 bytecode opcodes

This is a like Python 3.0's opcode.py with some classification
of stack usage.
"""
from xdis.opcodes.base import def_op, finalize_opcodes, format_extended_arg, init_opdata, jrel_op, rm_op, update_pj2
from xdis.opcodes.opcode_3x import format_MAKE_FUNCTION_arg
import xdis.opcodes.opcode_31 as opcode_31
version = 3.0
l = locals()
init_opdata(l, opcode_31, version)
rm_op(l, 'JUMP_IF_FALSE_OR_POP', 111)
rm_op(l, 'JUMP_IF_TRUE_OR_POP', 112)
rm_op(l, 'POP_JUMP_IF_FALSE', 114)
rm_op(l, 'POP_JUMP_IF_TRUE', 115)
rm_op(l, 'LIST_APPEND', 145)
rm_op(l, 'MAP_ADD', 147)
def_op(l, 'SET_ADD', 17, 2, 0)
def_op(l, 'LIST_APPEND', 18, 2, 0)
jrel_op(l, 'JUMP_IF_FALSE', 111, 1, 1)
jrel_op(l, 'JUMP_IF_TRUE', 112, 1, 1)
update_pj2(globals(), l)
opcode_arg_fmt = {'MAKE_FUNCTION': format_MAKE_FUNCTION_arg, 'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)