# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_16.py
# Compiled at: 2020-04-24 01:34:41
"""
CPython 1.6 bytecode opcodes

This is used in bytecode disassembly. This is similar to the
opcodes in Python's dis.py library.
"""
from xdis.cross_dis import findlabels, findlinestarts
import xdis.opcodes.opcode_15 as opcode_15
from xdis.opcodes.base import init_opdata, nargs_op, finalize_opcodes, format_extended_arg, update_pj2
version = 1.6
l = locals()
init_opdata(l, opcode_15, version)
nargs_op(l, 'CALL_FUNCTION_VAR', 140, -1, 1)
nargs_op(l, 'CALL_FUNCTION_KW', 141, -1, 1)
nargs_op(l, 'CALL_FUNCTION_VAR_KW', 142, -1, 1)
update_pj2(globals(), l)
opcode_arg_fmt = {'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)