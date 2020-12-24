# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_26pypy.py
# Compiled at: 2018-05-18 19:52:22
"""
PYPY 2.6 opcodes

This is a like Python 2.6's opcode.py with some classification
of stack usage.
"""
import xdis.opcodes.opcode_26 as opcode_26
from xdis.opcodes.base import finalize_opcodes, init_opdata, jrel_op, name_op, nargs_op, varargs_op, update_pj2
version = 2.6
l = locals()
init_opdata(l, opcode_26, version, is_pypy=True)
name_op(l, 'LOOKUP_METHOD', 201, 1, 2)
nargs_op(l, 'CALL_METHOD', 202, -1, 1)
l['hasnargs'].append(202)
varargs_op(l, 'BUILD_LIST_FROM_ARG', 203)
jrel_op(l, 'JUMP_IF_NOT_DEBUG', 204, conditional=True)
update_pj2(globals(), l)
finalize_opcodes(l)