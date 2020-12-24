# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_3x.py
# Compiled at: 2020-04-24 01:34:41
"""
CPython 3.2 bytecode opcodes to be used as a base for other opcodes including 3.2.

This is used in bytecode disassembly among other things. This is
similar to the opcodes in Python's opcode.py library.

If this file changes the other opcode files may have to a adjusted accordingly.
"""
from xdis.opcodes.base import compare_op, const_op, def_op, format_extended_arg, free_op, jabs_op, jrel_op, local_op, name_op, nargs_op, store_op, varargs_op
l = locals()
hascompare = []
hascondition = []
hasconst = []
hasfree = []
hasjabs = []
hasjrel = []
haslocal = []
hasname = []
hasnargs = []
hasstore = []
hasvargs = []
nofollow = []
opmap = {}
opname = [
 ''] * 256
oppush = [
 0] * 256
oppop = [
 0] * 256
for op in range(256):
    opname[op] = '<%r>' % (op,)

del op
def_op(l, 'STOP_CODE', 0, 0, 0, fallthrough=False)
def_op(l, 'POP_TOP', 1, 1, 0)
def_op(l, 'ROT_TWO', 2, 2, 2)
def_op(l, 'ROT_THREE', 3, 3, 3)
def_op(l, 'DUP_TOP', 4, 0, 1)
def_op(l, 'DUP_TOP_TWO', 5, 0, 2)
def_op(l, 'NOP', 9)
def_op(l, 'UNARY_POSITIVE', 10, 1, 1)
def_op(l, 'UNARY_NEGATIVE', 11, 1, 1)
def_op(l, 'UNARY_NOT', 12, 1, 1)
def_op(l, 'UNARY_INVERT', 15, 1, 1)
def_op(l, 'BINARY_POWER', 19, 2, 1)
def_op(l, 'BINARY_MULTIPLY', 20, 2, 1)
def_op(l, 'BINARY_MODULO', 22, 2, 1)
def_op(l, 'BINARY_ADD', 23, 2, 1)
def_op(l, 'BINARY_SUBTRACT', 24, 2, 1)
def_op(l, 'BINARY_SUBSCR', 25, 2, 1)
def_op(l, 'BINARY_FLOOR_DIVIDE', 26, 2, 1)
def_op(l, 'BINARY_TRUE_DIVIDE', 27, 2, 1)
def_op(l, 'INPLACE_FLOOR_DIVIDE', 28, 2, 1)
def_op(l, 'INPLACE_TRUE_DIVIDE', 29, 2, 1)
store_op(l, 'STORE_MAP', 54, 3, 1)
def_op(l, 'INPLACE_ADD', 55, 2, 1)
def_op(l, 'INPLACE_SUBTRACT', 56, 2, 1)
def_op(l, 'INPLACE_MULTIPLY', 57, 2, 1)
def_op(l, 'INPLACE_MODULO', 59, 2, 1)
store_op(l, 'STORE_SUBSCR', 60, 3, 0)
def_op(l, 'DELETE_SUBSCR', 61, 2, 0)
def_op(l, 'BINARY_LSHIFT', 62, 2, 1)
def_op(l, 'BINARY_RSHIFT', 63, 2, 1)
def_op(l, 'BINARY_AND', 64, 2, 1)
def_op(l, 'BINARY_XOR', 65, 2, 1)
def_op(l, 'BINARY_OR', 66, 2, 1)
def_op(l, 'INPLACE_POWER', 67, 2, 1)
def_op(l, 'GET_ITER', 68, 1, 1)
store_op(l, 'STORE_LOCALS', 69, 1, 0)
def_op(l, 'PRINT_EXPR', 70, 1, 0)
def_op(l, 'LOAD_BUILD_CLASS', 71, 0, 1)
def_op(l, 'INPLACE_LSHIFT', 75, 2, 1)
def_op(l, 'INPLACE_RSHIFT', 76, 2, 1)
def_op(l, 'INPLACE_AND', 77, 2, 1)
def_op(l, 'INPLACE_XOR', 78, 2, 1)
def_op(l, 'INPLACE_OR', 79, 2, 1)
def_op(l, 'BREAK_LOOP', 80, 0, 0, fallthrough=False)
def_op(l, 'WITH_CLEANUP', 81, 1, 0)
def_op(l, 'RETURN_VALUE', 83, 1, 0, fallthrough=False)
def_op(l, 'IMPORT_STAR', 84, 1, 0)
def_op(l, 'YIELD_VALUE', 86, 1, 1)
def_op(l, 'POP_BLOCK', 87, 0, 0)
def_op(l, 'END_FINALLY', 88, 1, 0)
def_op(l, 'POP_EXCEPT', 89, 0, 0)
HAVE_ARGUMENT = 90
store_op(l, 'STORE_NAME', 90, 1, 0, is_type='name')
name_op(l, 'DELETE_NAME', 91, 0, 0)
varargs_op(l, 'UNPACK_SEQUENCE', 92, 0, -1)
jrel_op(l, 'FOR_ITER', 93, 0, 1)
varargs_op(l, 'UNPACK_EX', 94, 0, 0)
store_op(l, 'STORE_ATTR', 95, 2, 0, is_type='name')
name_op(l, 'DELETE_ATTR', 96, 1, 0)
store_op(l, 'STORE_GLOBAL', 97, 1, 0, is_type='name')
name_op(l, 'DELETE_GLOBAL', 98, 0, 0)
const_op(l, 'LOAD_CONST', 100, 0, 1)
name_op(l, 'LOAD_NAME', 101, 0, 1)
varargs_op(l, 'BUILD_TUPLE', 102, -1, 1)
varargs_op(l, 'BUILD_LIST', 103, -1, 1)
varargs_op(l, 'BUILD_SET', 104, -1, 1)
def_op(l, 'BUILD_MAP', 105, 0, 1)
name_op(l, 'LOAD_ATTR', 106, 1, 1)
compare_op(l, 'COMPARE_OP', 107, 2, 1)
name_op(l, 'IMPORT_NAME', 108, 2, 1)
name_op(l, 'IMPORT_FROM', 109, 0, 1)
jrel_op(l, 'JUMP_FORWARD', 110, 0, 0, fallthrough=False)
jabs_op(l, 'JUMP_IF_FALSE_OR_POP', 111, conditional=True)
jabs_op(l, 'JUMP_IF_TRUE_OR_POP', 112, conditional=True)
jabs_op(l, 'JUMP_ABSOLUTE', 113, 0, 0, fallthrough=False)
jabs_op(l, 'POP_JUMP_IF_FALSE', 114, 2, 1, conditional=True)
jabs_op(l, 'POP_JUMP_IF_TRUE', 115, 2, 1, conditional=True)
name_op(l, 'LOAD_GLOBAL', 116, 0, 1)
jabs_op(l, 'CONTINUE_LOOP', 119, 0, 0, fallthrough=False)
jrel_op(l, 'SETUP_LOOP', 120, 0, 0, conditional=True)
jrel_op(l, 'SETUP_EXCEPT', 121, 0, 6, conditional=True)
jrel_op(l, 'SETUP_FINALLY', 122, 0, 6, conditional=True)
local_op(l, 'LOAD_FAST', 124, 0, 1)
store_op(l, 'STORE_FAST', 125, 1, 0, is_type='local')
local_op(l, 'DELETE_FAST', 126, 0, 0)
nargs_op(l, 'RAISE_VARARGS', 130, -1, 1, fallthrough=False)
nargs_op(l, 'CALL_FUNCTION', 131, -1, 1)
nargs_op(l, 'MAKE_FUNCTION', 132, -2, 1)
varargs_op(l, 'BUILD_SLICE', 133, 2, 1)
nargs_op(l, 'MAKE_CLOSURE', 134, -3, 1)
free_op(l, 'LOAD_CLOSURE', 135, 0, 1)
free_op(l, 'LOAD_DEREF', 136, 0, 1)
store_op(l, 'STORE_DEREF', 137, 1, 0, is_type='free')
free_op(l, 'DELETE_DEREF', 138, 0, 0)
nargs_op(l, 'CALL_FUNCTION_VAR', 140, -2, 1)
nargs_op(l, 'CALL_FUNCTION_KW', 141, -2, 1)
nargs_op(l, 'CALL_FUNCTION_VAR_KW', 142, -3, 1)
jrel_op(l, 'SETUP_WITH', 143, 0, 7)
def_op(l, 'LIST_APPEND', 145, 2, 1)
def_op(l, 'SET_ADD', 146, 1, 0)
def_op(l, 'MAP_ADD', 147, 3, 1)
def_op(l, 'EXTENDED_ARG', 144, 0, 0)
EXTENDED_ARG = 144

def format_MAKE_FUNCTION_arg(argc):
    pos_args = argc & 255
    name_default = argc >> 8 & 255
    annotate_args = argc >> 16 & 32767
    return '%d positional, %d name and default, %d annotations' % (pos_args, name_default, annotate_args)


opcode_arg_fmt = {'EXTENDED_ARG': format_extended_arg}