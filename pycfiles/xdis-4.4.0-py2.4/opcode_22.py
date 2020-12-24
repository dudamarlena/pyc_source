# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_22.py
# Compiled at: 2020-04-18 17:55:45
"""
CPython 2.2 bytecode opcodes

This is similar to the opcode portion in Python 2.2's dis.py library.
"""
import xdis.opcodes.opcode_2x as opcode_2x
from xdis.opcodes.base import def_op, init_opdata, finalize_opcodes, format_extended_arg, update_pj2
version = 2.2
l = locals()
init_opdata(l, opcode_2x, version)
def_op(l, 'FOR_LOOP', 114)
def_op(l, 'SET_LINENO', 127, 0, 0)
update_pj2(globals(), l)
opcode_arg_fmt = {'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)