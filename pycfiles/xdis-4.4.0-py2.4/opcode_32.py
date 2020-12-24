# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_32.py
# Compiled at: 2017-06-18 15:47:28
"""
CPython 3.2 bytecode opcodes

This is a like Python 3.2's opcode.py with some classification
of stack usage.
"""
import xdis.opcodes.opcode_3x as opcode_3x
from xdis.opcodes.base import finalize_opcodes, format_extended_arg, init_opdata, update_pj3
from xdis.opcodes.opcode_3x import format_MAKE_FUNCTION_arg
version = 3.2
l = locals()
init_opdata(l, opcode_3x, version)
update_pj3(globals(), l)
opcode_arg_fmt = {'MAKE_FUNCTION': format_MAKE_FUNCTION_arg, 'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)