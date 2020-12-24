# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_26.py
# Compiled at: 2020-04-18 17:55:45
"""
CPython 2.6 bytecode opcodes

This is a like Python 2.6's opcode.py with some classification
of stack usage.
"""
from xdis.opcodes.base import store_op, finalize_opcodes, format_extended_arg, init_opdata, update_pj2
import xdis.opcodes.opcode_25 as opcode_25
version = 2.6
l = locals()
init_opdata(l, opcode_25, version)
store_op(l, 'STORE_MAP', 54, 3, 1)
update_pj2(globals(), l)
opcode_arg_fmt = {'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)