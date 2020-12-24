# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_27.py
# Compiled at: 2020-04-18 17:55:45
"""
CPython 2.7 bytecode opcodes

This is a like Python 2.7's opcode.py with some classification
of stack usage.
"""
from xdis.opcodes.base import compare_op, def_op, finalize_opcodes, format_CALL_FUNCTION_pos_name_encoded, format_extended_arg, init_opdata, jabs_op, jrel_op, name_op, rm_op, update_pj3
import xdis.opcodes.opcode_26 as opcode_26
version = 2.7
l = locals()
init_opdata(l, opcode_26, version)
rm_op(l, 'BUILD_MAP', 104)
rm_op(l, 'LOAD_ATTR', 105)
rm_op(l, 'COMPARE_OP', 106)
rm_op(l, 'IMPORT_NAME', 107)
rm_op(l, 'IMPORT_FROM', 108)
rm_op(l, 'JUMP_IF_FALSE', 111)
rm_op(l, 'EXTENDED_ARG', 143)
rm_op(l, 'JUMP_IF_TRUE', 112)
def_op(l, 'LIST_APPEND', 94, 2, 1)
def_op(l, 'BUILD_SET', 104)
def_op(l, 'BUILD_MAP', 105)
name_op(l, 'LOAD_ATTR', 106)
compare_op(l, 'COMPARE_OP', 107)
name_op(l, 'IMPORT_NAME', 108, 2, 1)
name_op(l, 'IMPORT_FROM', 109, 0, 1)
jabs_op(l, 'JUMP_IF_FALSE_OR_POP', 111)
jabs_op(l, 'JUMP_IF_TRUE_OR_POP', 112)
jabs_op(l, 'POP_JUMP_IF_FALSE', 114)
jabs_op(l, 'POP_JUMP_IF_TRUE', 115)
jrel_op(l, 'SETUP_WITH', 143, 0, 2)
def_op(l, 'EXTENDED_ARG', 145)
def_op(l, 'SET_ADD', 146, 1, 0)
def_op(l, 'MAP_ADD', 147, 2, 1)
update_pj3(globals(), l)
opcode_arg_fmt = {'EXTENDED_ARG': format_extended_arg, 'CALL_FUNCTION': format_CALL_FUNCTION_pos_name_encoded}
finalize_opcodes(l)