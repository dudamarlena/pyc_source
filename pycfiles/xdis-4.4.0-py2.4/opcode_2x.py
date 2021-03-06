# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/opcodes/opcode_2x.py
# Compiled at: 2020-04-20 10:24:57
"""CPython core set of bytecode opcodes based on version 2.3

This is used in bytecode disassembly among other things. This is
similar to the opcodes in Python's opcode.py library.

If this file changes the other opcode files may have to be adjusted accordingly.
"""
from xdis.opcodes.base import compare_op, const_op, def_op, free_op, jabs_op, jrel_op, local_op, name_op, nargs_op, store_op, varargs_op
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
def_op(l, 'ROT_FOUR', 5, 4, 4)
def_op(l, 'UNARY_POSITIVE', 10, 1, 1)
def_op(l, 'UNARY_NEGATIVE', 11, 1, 1)
def_op(l, 'UNARY_NOT', 12, 1, 1)
def_op(l, 'UNARY_CONVERT', 13, 1, 1)
def_op(l, 'UNARY_INVERT', 15, 1, 1)
def_op(l, 'BINARY_POWER', 19, 2, 1)
def_op(l, 'BINARY_MULTIPLY', 20, 2, 1)
def_op(l, 'BINARY_DIVIDE', 21, 2, 1)
def_op(l, 'BINARY_MODULO', 22, 2, 1)
def_op(l, 'BINARY_ADD', 23, 2, 1)
def_op(l, 'BINARY_SUBTRACT', 24, 2, 1)
def_op(l, 'BINARY_SUBSCR', 25, 2, 1)
def_op(l, 'BINARY_FLOOR_DIVIDE', 26, 2, 1)
def_op(l, 'BINARY_TRUE_DIVIDE', 27, 2, 1)
def_op(l, 'INPLACE_FLOOR_DIVIDE', 28, 2, 1)
def_op(l, 'INPLACE_TRUE_DIVIDE', 29, 2, 1)
def_op(l, 'SLICE+0', 30, 1, 1)
def_op(l, 'SLICE+1', 31, 2, 1)
def_op(l, 'SLICE+2', 32, 2, 1)
def_op(l, 'SLICE+3', 33, 3, 1)
store_op(l, 'STORE_SLICE+0', 40, 2, 0)
store_op(l, 'STORE_SLICE+1', 41, 3, 0)
store_op(l, 'STORE_SLICE+2', 42, 3, 0)
store_op(l, 'STORE_SLICE+3', 43, 4, 0)
def_op(l, 'DELETE_SLICE+0', 50, 1, 0)
def_op(l, 'DELETE_SLICE+1', 51, 2, 0)
def_op(l, 'DELETE_SLICE+2', 52, 2, 0)
def_op(l, 'DELETE_SLICE+3', 53, 3, 0)
def_op(l, 'INPLACE_ADD', 55, 2, 1)
def_op(l, 'INPLACE_SUBTRACT', 56, 2, 1)
def_op(l, 'INPLACE_MULTIPLY', 57, 2, 1)
def_op(l, 'INPLACE_DIVIDE', 58, 2, 1)
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
def_op(l, 'PRINT_EXPR', 70, 1, 0)
def_op(l, 'PRINT_ITEM', 71, 1, 0)
def_op(l, 'PRINT_NEWLINE', 72, 1, 0)
def_op(l, 'PRINT_ITEM_TO', 73, 1, 0)
def_op(l, 'PRINT_NEWLINE_TO', 74, 1, 0)
def_op(l, 'INPLACE_LSHIFT', 75, 2, 1)
def_op(l, 'INPLACE_RSHIFT', 76, 2, 1)
def_op(l, 'INPLACE_AND', 77, 2, 1)
def_op(l, 'INPLACE_XOR', 78, 2, 1)
def_op(l, 'INPLACE_OR', 79, 2, 1)
def_op(l, 'BREAK_LOOP', 80, 0, 0, fallthrough=False)
def_op(l, 'LOAD_LOCALS', 82, 0, 1)
def_op(l, 'RETURN_VALUE', 83, 1, 0, fallthrough=False)
def_op(l, 'IMPORT_STAR', 84, 1, 0)
def_op(l, 'EXEC_STMT', 85, 3, 0)
def_op(l, 'YIELD_VALUE', 86, 1, 1)
def_op(l, 'POP_BLOCK', 87, 0, 0)
def_op(l, 'END_FINALLY', 88, 1, 0)
def_op(l, 'BUILD_CLASS', 89, 3, 0)
HAVE_ARGUMENT = 90
store_op(l, 'STORE_NAME', 90, 1, 0, is_type='name')
name_op(l, 'DELETE_NAME', 91, 0, 0)
varargs_op(l, 'UNPACK_SEQUENCE', 92, 9, 1)
jrel_op(l, 'FOR_ITER', 93, 9, 1)
store_op(l, 'STORE_ATTR', 95, 2, 0, is_type='name')
name_op(l, 'DELETE_ATTR', 96, 1, 0)
store_op(l, 'STORE_GLOBAL', 97, 1, 0, is_type='name')
name_op(l, 'DELETE_GLOBAL', 98, 0, 0)
def_op(l, 'DUP_TOPX', 99, 1, -1)
const_op(l, 'LOAD_CONST', 100, 0, 1)
name_op(l, 'LOAD_NAME', 101, 0, 1)
varargs_op(l, 'BUILD_TUPLE', 102, 9, 1)
varargs_op(l, 'BUILD_LIST', 103, 9, 1)
varargs_op(l, 'BUILD_MAP', 104, 0, 1)
name_op(l, 'LOAD_ATTR', 105, 1, 1)
compare_op(l, 'COMPARE_OP', 106, 2, 1)
name_op(l, 'IMPORT_NAME', 107, 2, 1)
name_op(l, 'IMPORT_FROM', 108, 0, 1)
jrel_op(l, 'JUMP_FORWARD', 110, 0, 0, fallthrough=False)
jrel_op(l, 'JUMP_IF_FALSE', 111, 1, 1, True)
jrel_op(l, 'JUMP_IF_TRUE', 112, 1, 1, True)
jabs_op(l, 'JUMP_ABSOLUTE', 113, 0, 0, fallthrough=False)
name_op(l, 'LOAD_GLOBAL', 116, 0, 1)
jabs_op(l, 'CONTINUE_LOOP', 119, 0, 0, fallthrough=False)
jrel_op(l, 'SETUP_LOOP', 120, 0, 0, conditional=True)
jrel_op(l, 'SETUP_EXCEPT', 121, 0, 6, conditional=True)
jrel_op(l, 'SETUP_FINALLY', 122, 0, 7, conditional=True)
local_op(l, 'LOAD_FAST', 124, 0, 1)
store_op(l, 'STORE_FAST', 125, 1, 0, is_type='local')
local_op(l, 'DELETE_FAST', 126)
def_op(l, 'RAISE_VARARGS', 130, -1, 0, fallthrough=False)
nargs_op(l, 'CALL_FUNCTION', 131, 9, 1)
def_op(l, 'MAKE_FUNCTION', 132, 9, 1)
varargs_op(l, 'BUILD_SLICE', 133, 9, 1)
def_op(l, 'MAKE_CLOSURE', 134, 9, 1)
free_op(l, 'LOAD_CLOSURE', 135, 0, 1)
free_op(l, 'LOAD_DEREF', 136, 0, 1)
store_op(l, 'STORE_DEREF', 137, 1, 0, is_type='free')
nargs_op(l, 'CALL_FUNCTION_VAR', 140, -1, 1)
nargs_op(l, 'CALL_FUNCTION_KW', 141, -1, 1)
nargs_op(l, 'CALL_FUNCTION_VAR_KW', 142, -1, 1)
def_op(l, 'EXTENDED_ARG', 143)
EXTENDED_ARG = 143