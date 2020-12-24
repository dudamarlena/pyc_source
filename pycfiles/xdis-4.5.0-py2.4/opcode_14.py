# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_14.py
# Compiled at: 2020-04-24 01:34:41
"""
CPython 1.4 bytecode opcodes

This is used in bytecode disassembly. This is similar to the
opcodes in Python's dis.py library.
"""
from xdis.cross_dis import findlabels
import xdis.opcodes.opcode_15 as opcode_15
from xdis.opcodes.base import init_opdata, def_op, name_op, varargs_op, finalize_opcodes, format_extended_arg, update_pj2
version = 1.4
l = locals()
init_opdata(l, opcode_15, version)
def_op(l, 'UNARY_CALL', 14)
def_op(l, 'BINARY_CALL', 26)
def_op(l, 'RAISE_EXCEPTION', 81)
def_op(l, 'BUILD_FUNCTION', 86)
varargs_op(l, 'UNPACK_ARG', 94)
varargs_op(l, 'UNPACK_VARARG', 99)
name_op(l, 'LOAD_LOCAL', 115)
varargs_op(l, 'SET_FUNC_ARGS', 117)
varargs_op(l, 'RESERVE_FAST', 123)
update_pj2(globals(), l)
opcode_arg_fmt = {'EXTENDED_ARG': format_extended_arg}
finalize_opcodes(l)

def findlinestarts(co, dup_lines=False):
    code = co.co_code
    n = len(code)
    offset = 0
    while offset < n:
        op = code[offset]
        offset += 1
        if op == l['opmap']['SET_LINENO'] and offset > 0:
            lineno = code[offset] + code[(offset + 1)] * 256
            yield (offset - 1, lineno)
        if op >= l['HAVE_ARGUMENT']:
            offset += 2