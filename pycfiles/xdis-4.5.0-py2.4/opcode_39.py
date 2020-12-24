# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_39.py
# Compiled at: 2020-04-24 01:34:41
"""
CPython 3.8 bytecode opcodes

This is a like Python 3.9's opcode.py
"""
from xdis.opcodes.base import const_op, def_op, finalize_opcodes, init_opdata, rm_op, update_pj3
from xdis.opcodes.opcode_36 import format_CALL_FUNCTION_EX, format_CALL_FUNCTION_KW, format_extended_arg36
import xdis.opcodes.opcode_38 as opcode_38
version = 3.9
l = locals()
init_opdata(l, opcode_38, version)
rm_op(l, 'BEGIN_FINALLY', 53)
rm_op(l, 'WITH_CLEANUP_START', 81)
rm_op(l, 'WITH_CLEANUP_FINISH', 82)
rm_op(l, 'END_FINALLY', 88)
rm_op(l, 'CALL_FINALLY', 162)
rm_op(l, 'POP_FINALLY', 163)
def_op(l, 'RERAISE', 48, 3, 0)
def_op(l, 'WITH_EXCEPT_START', 49, 0, 1)
def_op(l, 'LOAD_ASSERTION_ERROR', 74, 0, 1)
format_MAKE_FUNCTION_arg = opcode_38.format_MAKE_FUNCTION_arg
format_value_flags = opcode_38.format_value_flags
opcode_arg_fmt = {'CALL_FUNCTION_KW': format_CALL_FUNCTION_KW, 'CALL_FUNCTION_EX': format_CALL_FUNCTION_EX, 'MAKE_FUNCTION': format_MAKE_FUNCTION_arg, 'FORMAT_VALUE': format_value_flags, 'EXTENDED_ARG': format_extended_arg36}
update_pj3(globals(), l)
finalize_opcodes(l)