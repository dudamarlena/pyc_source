# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_21.py
# Compiled at: 2020-04-18 17:55:45
"""
CPython 2.1 bytecode opcodes

This is similar to the opcode portion in Python 2.1's dis.py library.
"""
import xdis.opcodes.opcode_22 as opcode_22
from xdis.opcodes.base import init_opdata, finalize_opcodes, format_extended_arg, rm_op, update_pj2
version = 2.1
l = locals()
init_opdata(l, opcode_22, version)
rm_op(l, 'BINARY_FLOOR_DIVIDE', 26)
rm_op(l, 'BINARY_TRUE_DIVIDE', 27)
rm_op(l, 'INPLACE_FLOOR_DIVIDE', 28)
rm_op(l, 'INPLACE_TRUE_DIVIDE', 29)
rm_op(l, 'GET_ITER', 68)
rm_op(l, 'YIELD_VALUE', 86)
rm_op(l, 'FOR_ITER', 93)
update_pj2(globals(), l)
opcode_arg_fmt = {'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)