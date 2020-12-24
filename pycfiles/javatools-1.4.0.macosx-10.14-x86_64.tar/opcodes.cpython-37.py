# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/opcodes.py
# Compiled at: 2018-10-18 16:07:18
# Size of source mod 2**32: 15504 bytes
"""
A module to hold all the Java opcodes. Data taken from publicly
available sources (see following for more information)

References
----------
* http://java.sun.com/docs/books/jvms/second_edition/html/VMSpecTOC.doc.html

:author: Christopher O'Brien  <obriencj@gmail.com>
:license: LGPL v.3
"""
from functools import partial
from six.moves import range
from .pack import compile_struct
__all__ = ('get_opcode_by_name', 'get_opname_by_code', 'get_arg_format', 'has_const_arg',
           'disassemble', 'OP_aaload', 'OP_aastore', 'OP_aconst_null', 'OP_aload',
           'OP_aload_0', 'OP_aload_1', 'OP_aload_2', 'OP_aload_3', 'OP_anewarray',
           'OP_areturn', 'OP_arraylength', 'OP_astore', 'OP_astore_0', 'OP_astore_1',
           'OP_astore_2', 'OP_astore_3', 'OP_athrow', 'OP_baload', 'OP_bastore',
           'OP_bipush', 'OP_caload', 'OP_castore', 'OP_checkcast', 'OP_d2f', 'OP_d2i',
           'OP_d2l', 'OP_dadd', 'OP_daload', 'OP_dastore', 'OP_dcmpg', 'OP_dcmpl',
           'OP_dconst_0', 'OP_dconst_1', 'OP_ddiv', 'OP_dload', 'OP_dload_0', 'OP_dload_1',
           'OP_dload_2', 'OP_dload_3', 'OP_dmul', 'OP_dneg', 'OP_drem', 'OP_dreturn',
           'OP_dstore', 'OP_dstore_0', 'OP_dstore_1', 'OP_dstore_2', 'OP_dstore_3',
           'OP_dsub', 'OP_dup', 'OP_dup2', 'OP_dup2_x1', 'OP_dup2_x2', 'OP_dup_x1',
           'OP_dup_x2', 'OP_f2d', 'OP_f2i', 'OP_f2l', 'OP_fadd', 'OP_faload', 'OP_fastore',
           'OP_fcmpg', 'OP_fcmpl', 'OP_fconst_0', 'OP_fconst_1', 'OP_fconst_2', 'OP_fdiv',
           'OP_fload', 'OP_fload_0', 'OP_fload_1', 'OP_fload_2', 'OP_fload_3', 'OP_fmul',
           'OP_fneg', 'OP_frem', 'OP_freturn', 'OP_fstore', 'OP_fstore_0', 'OP_fstore_1',
           'OP_fstore_2', 'OP_fstore_3', 'OP_fsub', 'OP_getfield', 'OP_getstatic',
           'OP_goto', 'OP_goto_w', 'OP_i2b', 'OP_i2c', 'OP_i2d', 'OP_i2f', 'OP_i2l',
           'OP_i2s', 'OP_iadd', 'OP_iaload', 'OP_iand', 'OP_iastore', 'OP_iconst_0',
           'OP_iconst_1', 'OP_iconst_2', 'OP_iconst_3', 'OP_iconst_4', 'OP_iconst_5',
           'OP_iconst_m1', 'OP_idiv', 'OP_if_acmpeq', 'OP_if_acmpne', 'OP_if_icmpeq',
           'OP_if_icmpge', 'OP_if_icmpgt', 'OP_if_icmple', 'OP_if_icmplt', 'OP_if_icmpne',
           'OP_ifeq', 'OP_ifge', 'OP_ifgt', 'OP_ifle', 'OP_iflt', 'OP_ifne', 'OP_ifnonnull',
           'OP_ifnull', 'OP_iinc', 'OP_iload', 'OP_iload_0', 'OP_iload_1', 'OP_iload_2',
           'OP_iload_3', 'OP_imul', 'OP_ineg', 'OP_instanceof', 'OP_invokedynamic',
           'OP_invokeinterface', 'OP_invokespecial', 'OP_invokestatic', 'OP_invokevirtual',
           'OP_ior', 'OP_irem', 'OP_ireturn', 'OP_ishl', 'OP_ishr', 'OP_istore',
           'OP_istore_0', 'OP_istore_1', 'OP_istore_2', 'OP_istore_3', 'OP_isub',
           'OP_iushr', 'OP_ixor', 'OP_jsr', 'OP_jsr_w', 'OP_l2d', 'OP_l2f', 'OP_l2i',
           'OP_ladd', 'OP_laload', 'OP_land', 'OP_lastore', 'OP_lcmp', 'OP_lconst_0',
           'OP_lconst_1', 'OP_ldc', 'OP_ldc2_w', 'OP_ldc_w', 'OP_ldiv', 'OP_lload',
           'OP_lload_0', 'OP_lload_1', 'OP_lload_2', 'OP_lload_3', 'OP_lmul', 'OP_lneg',
           'OP_lookupswitch', 'OP_lor', 'OP_lrem', 'OP_lreturn', 'OP_lshl', 'OP_lshr',
           'OP_lstore', 'OP_lstore_0', 'OP_lstore_1', 'OP_lstore_2', 'OP_lstore_3',
           'OP_lsub', 'OP_lushr', 'OP_lxor', 'OP_monitorentry', 'OP_monitorexit',
           'OP_multianewarray', 'OP_new', 'OP_newarray', 'OP_nop', 'OP_pop', 'OP_pop2',
           'OP_putfield', 'OP_putstatic', 'OP_ret', 'OP_return', 'OP_saload', 'OP_sastore',
           'OP_sipush', 'OP_swap', 'OP_tableswitch', 'OP_wide')
__OPTABLE = {}
_OPINDEX_NAME = 0
_OPINDEX_VAL = 1
_OPINDEX_FMT = 2
_OPINDEX_CONSUME = 3
_OPINDEX_PRODUCE = 4
_OPINDEX_CONST = 5
_struct_i = compile_struct('>i')
_struct_ii = compile_struct('>ii')
_struct_iii = compile_struct('>iii')
_struct_BH = compile_struct('>BH')
_struct_BHh = compile_struct('>BHh')

def __op(name, val, fmt=None, const=False, consume=0, produce=0):
    """
    provides sensible defaults for a code, and registers it with the
    __OPTABLE for lookup.
    """
    name = name.lower()
    if isinstance(fmt, str):
        fmt = partial(_unpack, compile_struct(fmt))
    operand = (name, val, fmt, consume, produce, const)
    assert name not in __OPTABLE
    assert val not in __OPTABLE
    __OPTABLE[name] = operand
    __OPTABLE[val] = operand
    return val


def get_opcode_by_name(name):
    """
    get the integer opcode by its name
    """
    return __OPTABLE[name.lower()][_OPINDEX_VAL]


def get_opname_by_code(code):
    """
    get the name of an opcode
    """
    return __OPTABLE[code][_OPINDEX_NAME]


def get_arg_format(code):
    """
    get the format of arguments to this opcode
    """
    return __OPTABLE[code][_OPINDEX_FMT]


def has_const_arg(code):
    """
    which arg is a const for this opcode
    """
    return __OPTABLE[code][_OPINDEX_CONST]


def _unpack(struct, bc, offset=0):
    """
    returns the unpacked data tuple, and the next offset past the
    unpacked data
    """
    return (
     struct.unpack_from(bc, offset), offset + struct.size)


def _unpack_lookupswitch(bc, offset):
    """
    function for unpacking the lookupswitch op arguments
    """
    jump = offset % 4
    if jump:
        offset += 4 - jump
    (default, npairs), offset = _unpack(_struct_ii, bc, offset)
    switches = list()
    for _index in range(npairs):
        pair, offset = _unpack(_struct_ii, bc, offset)
        switches.append(pair)

    return ((default, switches), offset)


def _unpack_tableswitch(bc, offset):
    """
    function for unpacking the tableswitch op arguments
    """
    jump = offset % 4
    if jump:
        offset += 4 - jump
    (default, low, high), offset = _unpack(_struct_iii, bc, offset)
    joffs = list()
    for _index in range(high - low + 1):
        j, offset = _unpack(_struct_i, bc, offset)
        joffs.append(j)

    return ((default, low, high, joffs), offset)


def _unpack_wide(bc, offset):
    """
    unpacker for wide ops
    """
    code = ord(bc[offset])
    if code == OP_iinc:
        return _unpack(_struct_BHh, bc, offset)
    if code in (OP_iload, OP_fload, OP_aload, OP_lload, OP_dload,
     OP_istore, OP_fstore, OP_astore, OP_lstore,
     OP_dstore, OP_ret):
        return _unpack(_struct_BH, bc, offset)
    assert False


def disassemble(bytecode):
    """
    Generator. Disassembles Java bytecode into a sequence of (offset,
    code, args) tuples
    :type bytecode: bytes
    """
    offset = 0
    end = len(bytecode)
    while offset < end:
        orig_offset = offset
        code = bytecode[offset]
        if not isinstance(code, int):
            code = ord(code)
        offset += 1
        args = tuple()
        fmt = get_arg_format(code)
        if fmt:
            args, offset = fmt(bytecode, offset)
        yield (orig_offset, code, args)


OP_aaload = __op('aaload', 50)
OP_aastore = __op('aastore', 83)
OP_aconst_null = __op('aconst_null', 1)
OP_aload = __op('aload', 25, fmt='>B')
OP_aload_0 = __op('aload_0', 42)
OP_aload_1 = __op('aload_1', 43)
OP_aload_2 = __op('aload_2', 44)
OP_aload_3 = __op('aload_3', 45)
OP_anewarray = __op('anewarray', 189, fmt='>H', const=True)
OP_areturn = __op('areturn', 176)
OP_arraylength = __op('arraylength', 190)
OP_astore = __op('astore', 58, fmt='>B')
OP_astore_0 = __op('astore_0', 75)
OP_astore_1 = __op('astore_1', 76)
OP_astore_2 = __op('astore_2', 77)
OP_astore_3 = __op('astore_3', 78)
OP_athrow = __op('athrow', 191)
OP_baload = __op('baload', 51)
OP_bastore = __op('bastore', 84)
OP_bipush = __op('bipush', 16, fmt='>B')
OP_caload = __op('caload', 52)
OP_castore = __op('castore', 85)
OP_checkcast = __op('checkcast', 192, fmt='>H', const=True)
OP_d2f = __op('d2f', 144)
OP_d2i = __op('d2i', 142)
OP_d2l = __op('d2l', 143)
OP_dadd = __op('dadd', 99)
OP_daload = __op('daload', 49)
OP_dastore = __op('dastore', 82)
OP_dcmpg = __op('dcmpg', 152)
OP_dcmpl = __op('dcmpl', 151)
OP_dconst_0 = __op('dconst_0', 14)
OP_dconst_1 = __op('dconst_1', 15)
OP_ddiv = __op('ddiv', 111)
OP_dload = __op('dload', 24, fmt='>B')
OP_dload_0 = __op('dload_0', 38)
OP_dload_1 = __op('dload_1', 39)
OP_dload_2 = __op('dload_2', 40)
OP_dload_3 = __op('dload_3', 41)
OP_dmul = __op('dmul', 107)
OP_dneg = __op('dneg', 119)
OP_drem = __op('drem', 115)
OP_dreturn = __op('dreturn', 175)
OP_dstore = __op('dstore', 57, fmt='>B')
OP_dstore_0 = __op('dstore_0', 71)
OP_dstore_1 = __op('dstore_1', 72)
OP_dstore_2 = __op('dstore_2', 73)
OP_dstore_3 = __op('dstore_3', 74)
OP_dsub = __op('dsub', 103)
OP_dup = __op('dup', 89)
OP_dup_x1 = __op('dup_x1', 90)
OP_dup_x2 = __op('dup_x2', 91)
OP_dup2 = __op('dup2', 92)
OP_dup2_x1 = __op('dup2_x1', 93)
OP_dup2_x2 = __op('dup2_x2', 94)
OP_f2d = __op('f2d', 141)
OP_f2i = __op('f2i', 139)
OP_f2l = __op('f2l', 140)
OP_fadd = __op('fadd', 98)
OP_faload = __op('faload', 48)
OP_fastore = __op('fastore', 81)
OP_fcmpg = __op('fcmpg', 150)
OP_fcmpl = __op('fcmpl', 149)
OP_fconst_0 = __op('fconst_0', 11)
OP_fconst_1 = __op('fconst_1', 12)
OP_fconst_2 = __op('fconst_2', 13)
OP_fdiv = __op('fdiv', 110)
OP_fload = __op('fload', 23, fmt='>B')
OP_fload_0 = __op('fload_0', 34)
OP_fload_1 = __op('fload_1', 35)
OP_fload_2 = __op('fload_2', 36)
OP_fload_3 = __op('fload_3', 37)
OP_fmul = __op('fmul', 106)
OP_fneg = __op('fneg', 118)
OP_frem = __op('frem', 114)
OP_freturn = __op('freturn', 174)
OP_fstore = __op('fstore', 56, fmt='>B')
OP_fstore_0 = __op('fstore_0', 67)
OP_fstore_1 = __op('fstore_1', 68)
OP_fstore_2 = __op('fstore_2', 69)
OP_fstore_3 = __op('fstore_3', 70)
OP_fsub = __op('fsub', 102)
OP_getfield = __op('getfield', 180, fmt='>H', const=True)
OP_getstatic = __op('getstatic', 178, fmt='>H', const=True)
OP_goto = __op('goto', 167, fmt='>h')
OP_goto_w = __op('goto_w', 200, fmt='>i')
OP_i2b = __op('i2b', 145)
OP_i2c = __op('i2c', 146)
OP_i2d = __op('i2d', 135)
OP_i2f = __op('i2f', 134)
OP_i2l = __op('i2l', 133)
OP_i2s = __op('i2s', 147)
OP_iadd = __op('iadd', 96)
OP_iaload = __op('iaload', 46)
OP_iand = __op('iand', 126)
OP_iastore = __op('iastore', 79)
OP_iconst_m1 = __op('iconst_m1', 2)
OP_iconst_0 = __op('iconst_0', 3)
OP_iconst_1 = __op('iconst_1', 4)
OP_iconst_2 = __op('iconst_2', 5)
OP_iconst_3 = __op('iconst_3', 6)
OP_iconst_4 = __op('iconst_4', 7)
OP_iconst_5 = __op('iconst_5', 8)
OP_idiv = __op('idiv', 108)
OP_if_acmpeq = __op('if_acmpeq', 165, fmt='>h')
OP_if_acmpne = __op('if_acmpne', 166, fmt='>h')
OP_if_icmpeq = __op('if_icmpeq', 159, fmt='>h')
OP_if_icmpne = __op('if_icmpne', 160, fmt='>h')
OP_if_icmplt = __op('if_icmplt', 161, fmt='>h')
OP_if_icmpge = __op('if_icmpge', 162, fmt='>h')
OP_if_icmpgt = __op('if_icmpgt', 163, fmt='>h')
OP_if_icmple = __op('if_icmple', 164, fmt='>h')
OP_ifeq = __op('ifeq', 153, fmt='>h')
OP_ifne = __op('ifne', 154, fmt='>h')
OP_iflt = __op('iflt', 155, fmt='>h')
OP_ifge = __op('ifge', 156, fmt='>h')
OP_ifgt = __op('ifgt', 157, fmt='>h')
OP_ifle = __op('ifle', 158, fmt='>h')
OP_ifnonnull = __op('ifnonnull', 199, fmt='>h')
OP_ifnull = __op('ifnull', 198, fmt='>h')
OP_iinc = __op('iinc', 132, fmt='>Bb')
OP_iload = __op('iload', 21, fmt='>B')
OP_iload_0 = __op('iload_0', 26)
OP_iload_1 = __op('iload_1', 27)
OP_iload_2 = __op('iload_2', 28)
OP_iload_3 = __op('iload_3', 29)
OP_imul = __op('imul', 104)
OP_ineg = __op('ineg', 116)
OP_instanceof = __op('instanceof', 193, fmt='>H', const=True)
OP_invokedynamic = __op('invokedynamic', 186, fmt='>HBB', const=True)
OP_invokeinterface = __op('invokeinterface', 185, fmt='>HBB', const=True)
OP_invokespecial = __op('invokespecial', 183, fmt='>H', const=True)
OP_invokestatic = __op('invokestatic', 184, fmt='>H', const=True)
OP_invokevirtual = __op('invokevirtual', 182, fmt='>H', const=True)
OP_ior = __op('ior', 128)
OP_irem = __op('irem', 112)
OP_ireturn = __op('ireturn', 172)
OP_ishl = __op('ishl', 120)
OP_ishr = __op('ishr', 122)
OP_istore = __op('istore', 54, fmt='>B')
OP_istore_0 = __op('istore_0', 59)
OP_istore_1 = __op('istore_1', 60)
OP_istore_2 = __op('istore_2', 61)
OP_istore_3 = __op('istore_3', 62)
OP_isub = __op('isub', 100)
OP_iushr = __op('iushr', 124)
OP_ixor = __op('ixor', 130)
OP_jsr = __op('jsr', 168, fmt='>h')
OP_jsr_w = __op('jsr_w', 201, fmt='>i')
OP_l2d = __op('l2d', 138)
OP_l2f = __op('l2f', 137)
OP_l2i = __op('l2i', 136)
OP_ladd = __op('ladd', 97)
OP_laload = __op('laload', 47)
OP_land = __op('land', 127)
OP_lastore = __op('lastore', 80)
OP_lcmp = __op('lcmp', 148)
OP_lconst_0 = __op('lconst_0', 9)
OP_lconst_1 = __op('lconst_1', 10)
OP_ldc = __op('ldc', 18, fmt='>B', const=True)
OP_ldc_w = __op('ldc_w', 19, fmt='>H', const=True)
OP_ldc2_w = __op('ldc2_w', 20, fmt='>H', const=True)
OP_ldiv = __op('ldiv', 109)
OP_lload = __op('lload', 22, fmt='>B')
OP_lload_0 = __op('lload_0', 30)
OP_lload_1 = __op('lload_1', 31)
OP_lload_2 = __op('lload_2', 32)
OP_lload_3 = __op('lload_3', 33)
OP_lmul = __op('lmul', 105)
OP_lneg = __op('lneg', 117)
OP_lookupswitch = __op('lookupswitch', 171, fmt=_unpack_lookupswitch)
OP_lor = __op('lor', 129)
OP_lrem = __op('lrem', 113)
OP_lreturn = __op('lreturn', 173)
OP_lshl = __op('lshl', 121)
OP_lshr = __op('lshr', 123)
OP_lstore = __op('lstore', 55, fmt='>B')
OP_lstore_0 = __op('lstore_0', 63)
OP_lstore_1 = __op('lstore_1', 64)
OP_lstore_2 = __op('lstore_2', 65)
OP_lstore_3 = __op('lstore_3', 66)
OP_lsub = __op('lsub', 101)
OP_lushr = __op('lushr', 125)
OP_lxor = __op('lxor', 131)
OP_monitorentry = __op('monitorentry', 194)
OP_monitorexit = __op('monitorexit', 195)
OP_multianewarray = __op('multianewarray', 197, fmt='>HB')
OP_new = __op('new', 187, fmt='>H', const=True)
OP_newarray = __op('newarray', 188, fmt='>B')
OP_nop = __op('nop', 0)
OP_pop = __op('pop', 87)
OP_pop2 = __op('pop2', 88)
OP_putfield = __op('putfield', 181, fmt='>H', const=True)
OP_putstatic = __op('putstatic', 179, fmt='>H', const=True)
OP_ret = __op('ret', 169, fmt='>B')
OP_return = __op('return', 177)
OP_saload = __op('saload', 53)
OP_sastore = __op('sastore', 86)
OP_sipush = __op('sipush', 17, fmt='>h')
OP_swap = __op('swap', 95)
OP_tableswitch = __op('tableswitch', 170, fmt=_unpack_tableswitch)
OP_wide = __op('wide', 196, fmt=_unpack_wide)