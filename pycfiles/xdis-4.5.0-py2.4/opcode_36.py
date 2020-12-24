# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_36.py
# Compiled at: 2020-04-24 01:34:41
"""
CPython 3.6 bytecode opcodes

This is a like Python 3.6's opcode.py with some classification
of stack usage.
"""
from xdis.opcodes.base import def_op, finalize_opcodes, init_opdata, jrel_op, name_op, nargs_op, rm_op, store_op, varargs_op, update_pj3
import xdis.opcodes.opcode_35 as opcode_35
EXTENDED_ARG_SHIFT = 8
version = 3.6
l = locals()
init_opdata(l, opcode_35, version)
rm_op(l, 'MAKE_CLOSURE', 134)
rm_op(l, 'CALL_FUNCTION_VAR', 140)
rm_op(l, 'CALL_FUNCTION_VAR_KW', 142)
store_op(l, 'STORE_ANNOTATION', 127, 1, 0, is_type='name')
jrel_op(l, 'SETUP_ASYNC_WITH', 154, 2, 8)
def_op(l, 'FORMAT_VALUE', 155, 1, 1)
varargs_op(l, 'BUILD_CONST_KEY_MAP', 156, -2, 1)
nargs_op(l, 'CALL_FUNCTION_EX', 142, -2, 1)
def_op(l, 'SETUP_ANNOTATIONS', 85, 1, 1)
varargs_op(l, 'BUILD_STRING', 157, -2, 2)
varargs_op(l, 'BUILD_TUPLE_UNPACK_WITH_CALL', 158)
MAKE_FUNCTION_FLAGS = tuple(('default keyword-only annotation closure').split())

def format_MAKE_FUNCTION_arg(flags):
    pattr = ''
    for flag in MAKE_FUNCTION_FLAGS:
        bit = flags & 1
        if bit:
            if pattr:
                pattr += ', ' + flag
            else:
                pattr = flag
        flags >>= 1

    return pattr


def format_value_flags(flags):
    if flags & 3 == 0:
        return ''
    elif flags & 3 == 1:
        return '!s'
    elif flags & 3 == 2:
        return '!r'
    elif flags & 3 == 3:
        return '!a'
    elif flags & 4 == 4:
        return ''


def format_extended_arg36(arg):
    return str(arg * (1 << 8))


def format_CALL_FUNCTION_EX(flags):
    str = ''
    if flags & 1:
        str = 'keyword args'
    return str


def format_CALL_FUNCTION_KW(argc):
    return '%d total positional and keyword args' % argc


opcode_arg_fmt = {'CALL_FUNCTION_KW': format_CALL_FUNCTION_KW, 'CALL_FUNCTION_EX': format_CALL_FUNCTION_EX, 'MAKE_FUNCTION': format_MAKE_FUNCTION_arg, 'FORMAT_VALUE': format_value_flags, 'EXTENDED_ARG': format_extended_arg36}
update_pj3(globals(), l)
finalize_opcodes(l)