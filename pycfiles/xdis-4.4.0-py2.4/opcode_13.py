# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_13.py
# Compiled at: 2020-04-18 17:55:45
"""
CPython 1.3 bytecode opcodes

This is used in bytecode disassembly. This is similar to the
opcodes in Python's dis.py library.
"""
from xdis.bytecode import findlabels
import xdis.opcodes.opcode_14 as opcode_14
from xdis.opcodes.base import init_opdata, def_op, rm_op, finalize_opcodes, format_extended_arg, update_pj2
version = 1.3
l = locals()
init_opdata(l, opcode_14, version)
rm_op(l, 'BINARY_POWER', 19)
def_op(l, 'LOAD_GLOBALS', 84)
update_pj2(globals(), l)
opcode_arg_fmt = {'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)
findlinestarts = opcode_14.findlinestarts