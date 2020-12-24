# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_37.py
# Compiled at: 2020-04-24 01:34:41
"""
CPython 3.7 bytecode opcodes

This is a like Python 3.7's opcode.py with some classification
of stack usage.
"""
from xdis.opcodes.base import def_op, finalize_opcodes, init_opdata, nargs_op, jrel_op, name_op, rm_op, update_pj3
import xdis.opcodes.opcode_36 as opcode_36
version = 3.7
l = locals()
init_opdata(l, opcode_36, version)
rm_op(l, 'STORE_ANNOTATION', 127)
def_op(l, 'WITH_CLEANUP_START', 81, 0, 2)
def_op(l, 'WITH_CLEANUP_FINISH', 82, 3, 0)
def_op(l, 'END_FINALLY', 88, 6, 0)
def_op(l, 'POP_EXCEPT', 89, 3, 0)
jrel_op(l, 'SETUP_WITH', 143, 0, 6)
jrel_op(l, 'SETUP_ASYNC_WITH', 154, 0, 5)
name_op(l, 'LOAD_METHOD', 160, 0, 1)
nargs_op(l, 'CALL_METHOD', 161, -2, 1)
format_MAKE_FUNCTION_arg = opcode_36.format_MAKE_FUNCTION_arg
format_value_flags = opcode_36.format_value_flags
opcode_arg_fmt = {'CALL_FUNCTION_KW': opcode_36.format_CALL_FUNCTION_KW, 'CALL_FUNCTION_EX': opcode_36.format_CALL_FUNCTION_EX, 'MAKE_FUNCTION': format_MAKE_FUNCTION_arg, 'FORMAT_VALUE': format_value_flags, 'EXTENDED_ARG': opcode_36.format_extended_arg36}
update_pj3(globals(), l)
finalize_opcodes(l)