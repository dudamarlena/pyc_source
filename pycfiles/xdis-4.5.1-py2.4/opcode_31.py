# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_31.py
# Compiled at: 2020-04-26 21:30:10
"""
CPython 3.1 bytecode opcodes

This is a like Python 3.1's opcode.py with some classification
of stack usage.
"""
from xdis.opcodes.base import def_op, format_extended_arg, finalize_opcodes, init_opdata, name_op, rm_op, update_pj3
from xdis.opcodes.opcode_3x import format_MAKE_FUNCTION_arg
import xdis.opcodes.opcode_32 as opcode_32
l = locals()
version = 3.1
init_opdata(l, opcode_32, version)
rm_op(l, 'DUP_TOP_TWO', 5)
rm_op(l, 'DELETE_DEREF', 138)
rm_op(l, 'SETUP_WITH', 143)
name_op(l, 'IMPORT_NAME', 108, 1, 1)
def_op(l, 'ROT_FOUR', 5, 4, 4)
def_op(l, 'DUP_TOPX', 99, -1, 2)
def_op(l, 'EXTENDED_ARG', 143)
update_pj3(globals(), l)
opcode_arg_fmt = {'MAKE_FUNCTION': format_MAKE_FUNCTION_arg, 'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)