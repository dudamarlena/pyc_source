# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_33pypy.py
# Compiled at: 2020-04-18 17:55:45
"""
PYPY 3.3 opcodes

This is a like Python 3.3's opcode.py with some classification
of stack usage.
"""
from xdis.opcodes.base import finalize_opcodes, init_opdata, jrel_op, name_op, nargs_op, varargs_op, update_pj3
version = 3.3
import xdis.opcodes.opcode_33 as opcode_33
l = locals()
init_opdata(l, opcode_33, version, is_pypy=True)
name_op(l, 'LOOKUP_METHOD', 201, 1, 2)
nargs_op(l, 'CALL_METHOD', 202, -1, 1)
l['hasvargs'].append(202)
varargs_op(l, 'BUILD_LIST_FROM_ARG', 203)
jrel_op(l, 'JUMP_IF_NOT_DEBUG', 204, conditional=True)
update_pj3(globals(), l)
finalize_opcodes(l)