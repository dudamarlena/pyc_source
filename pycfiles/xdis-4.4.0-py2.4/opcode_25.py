# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_25.py
# Compiled at: 2017-06-18 15:47:28
"""
CPython 2.5 bytecode opcodes

This is a like Python 2.5's opcode.py with some classification
of stack usage.
"""
import xdis.opcodes.opcode_24 as opcode_24
from xdis.opcodes.base import def_op, init_opdata, finalize_opcodes, format_extended_arg, update_pj2
version = 2.5
l = locals()
init_opdata(l, opcode_24, version)
def_op(l, 'WITH_CLEANUP', 81)
update_pj2(globals(), l)
opcode_arg_fmt = {'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)