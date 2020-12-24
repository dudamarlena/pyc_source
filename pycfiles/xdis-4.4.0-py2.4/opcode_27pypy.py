# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_27pypy.py
# Compiled at: 2020-04-18 17:55:45
"""
PYPY 2.7 opcodes

This is a like Python 2.7's opcode.py with some classification
of stack usage.
"""
import xdis.opcodes.opcode_27 as opcode_27
from xdis.opcodes.base import def_op, finalize_opcodes, init_opdata, jrel_op, name_op, nargs_op, update_pj3
version = 2.7
l = locals()
init_opdata(l, opcode_27, version, is_pypy=True)
name_op(l, 'LOOKUP_METHOD', 201, 1, 2)
nargs_op(l, 'CALL_METHOD', 202, -1, 1)
l['hasnargs'].append(202)
def_op(l, 'BUILD_LIST_FROM_ARG', 203)
jrel_op(l, 'JUMP_IF_NOT_DEBUG', 204, conditional=True)
import sys
if sys.version_info[:3] >= (2, 7, 13) and sys.version_info[4] >= 42:
    def_op(l, 'LOAD_REVDB_VAR', 205)
update_pj3(globals(), l)
finalize_opcodes(l)