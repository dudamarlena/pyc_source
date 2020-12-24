# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_34.py
# Compiled at: 2020-04-24 01:34:41
"""
CPython 3.4 bytecode opcodes

This is a like Python 3.4's opcode.py with some classification
of stack usage.
"""
from xdis.opcodes.base import def_op, finalize_opcodes, format_extended_arg, free_op, init_opdata, rm_op, update_pj3
from xdis.opcodes.opcode_3x import format_MAKE_FUNCTION_arg
import xdis.opcodes.opcode_33 as opcode_33
version = 3.4
l = locals()
init_opdata(l, opcode_33, version)
rm_op(l, 'STORE_LOCALS', 69)
free_op(l, 'LOAD_CLASSDEREF', 148)
update_pj3(globals(), l)
opcode_arg_fmt = {'MAKE_FUNCTION': format_MAKE_FUNCTION_arg, 'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)