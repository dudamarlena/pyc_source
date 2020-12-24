# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_36pypy.py
# Compiled at: 2020-04-18 17:55:45
"""
PYPY 3.6 opcodes

This is a like Python 3.6's opcode.py with some classification
of stack usage.
"""
from xdis.opcodes.base import format_CALL_FUNCTION_pos_name_encoded, def_op, finalize_opcodes, format_extended_arg, init_opdata, jrel_op, name_op, nargs_op, rm_op, varargs_op, update_pj3
version = 3.6
from xdis.opcodes.opcode_3x import format_MAKE_FUNCTION_arg
import xdis.opcodes.opcode_36 as opcode_36
l = locals()
init_opdata(l, opcode_36, version, is_pypy=True)
rm_op(l, 'CALL_FUNCTION_EX', 142)
rm_op(l, 'BUILD_TUPLE_UNPACK_WITH_CALL', 158)
def_op(l, 'MAKE_CLOSURE', 134, 9, 1)
nargs_op(l, 'CALL_FUNCTION_VAR', 140, 9, 1)
nargs_op(l, 'CALL_FUNCTION_KW', 141, 9, 1)
nargs_op(l, 'CALL_FUNCTION_VAR_KW', 142, 9, 1)
name_op(l, 'LOOKUP_METHOD', 201, 1, 2)
nargs_op(l, 'CALL_METHOD', 202, -1, 1)
l['hasvargs'].append(202)
varargs_op(l, 'BUILD_LIST_FROM_ARG', 203)
jrel_op(l, 'JUMP_IF_NOT_DEBUG', 204, conditional=True)
import sys
if sys.version_info[:3] >= (3, 6, 1):
    def_op(l, 'LOAD_REVDB_VAR', 205)
update_pj3(globals(), l)
opcode_arg_fmt = {'MAKE_FUNCTION': format_MAKE_FUNCTION_arg, 'CALL_FUNCTION': format_CALL_FUNCTION_pos_name_encoded, 'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)