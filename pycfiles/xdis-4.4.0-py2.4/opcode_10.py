# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_10.py
# Compiled at: 2020-04-18 17:55:45
"""
CPython 1.0 bytecode opcodes

This is used in bytecode disassembly. This is similar to the
opcodes in Python's dis.py library.
"""
from xdis.bytecode import findlabels
import xdis.opcodes.opcode_11 as opcode_11
from xdis.opcodes.base import init_opdata, rm_op, finalize_opcodes, format_extended_arg, update_pj2
version = 1.0
l = locals()
init_opdata(l, opcode_11, version)
rm_op(l, 'LOAD_GLOBALS', 84)
rm_op(l, 'EXEC_STMT', 85)
update_pj2(globals(), l)
opcode_arg_fmt = {'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)
findlinestarts = opcode_11.findlinestarts