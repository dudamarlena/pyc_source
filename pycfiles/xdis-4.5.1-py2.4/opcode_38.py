# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_38.py
# Compiled at: 2020-04-24 01:34:41
"""
CPython 3.8 bytecode opcodes

This is a like Python 3.8's opcode.py
"""
from xdis.opcodes.base import finalize_opcodes, init_opdata, nargs_op, def_op, jrel_op, rm_op, update_pj3
import xdis.opcodes.opcode_37 as opcode_37
from xdis.opcodes.opcode_36 import format_CALL_FUNCTION_EX, format_CALL_FUNCTION_KW, format_extended_arg36
version = 3.8
l = locals()
init_opdata(l, opcode_37, version)
rm_op(l, 'BREAK_LOOP', 80)
rm_op(l, 'CONTINUE_LOOP', 119)
rm_op(l, 'SETUP_LOOP', 120)
rm_op(l, 'SETUP_EXCEPT', 121)
def_op(l, 'ROT_FOUR', 6, 4, 4)
def_op(l, 'BEGIN_FINALLY', 53, 0, 6)
def_op(l, 'END_ASYNC_FOR', 54, 7, 0)
def_op(l, 'END_FINALLY', 88, 6, 0)
jrel_op(l, 'CALL_FINALLY', 162, 0, 1)
nargs_op(l, 'POP_FINALLY', 163, 6, 0)
format_MAKE_FUNCTION_arg = opcode_37.format_MAKE_FUNCTION_arg
format_value_flags = opcode_37.format_value_flags
opcode_arg_fmt = {'CALL_FUNCTION_KW': format_CALL_FUNCTION_KW, 'CALL_FUNCTION_EX': format_CALL_FUNCTION_EX, 'MAKE_FUNCTION': format_MAKE_FUNCTION_arg, 'FORMAT_VALUE': format_value_flags, 'EXTENDED_ARG': format_extended_arg36}
update_pj3(globals(), l)
finalize_opcodes(l)