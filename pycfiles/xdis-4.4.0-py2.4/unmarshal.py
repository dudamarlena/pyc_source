# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/unmarshal.py
# Compiled at: 2020-04-20 10:24:57
"""CPython magic- and version-independent Python object
deserialization (unmarshal).

This is needed when the bytecode extracted is from
a different version than the currently-running Python.

When the running interpreter and the read-in bytecode are the same,
you can simply use Python's built-in marshal.loads() to produce a code
object
"""
import sys
from struct import unpack
from xdis.magics import magic_int2float
from xdis.codetype import to_portable
from xdis.version_info import PYTHON3, PYTHON_VERSION, IS_PYPY
internStrings = []
internObjects = []
if PYTHON3:

    def long(n):
        return n


else:
    import unicodedata
    if PYTHON_VERSION < 2.4:
        from sets import Set as set
        frozenset = set

def compat_str(s):
    if PYTHON3:
        try:
            return s.decode('utf-8')
        except UnicodeDecodeError:
            return s
        else:
            return s.decode()
    else:
        return str(s)


def compat_u2s(u):
    if PYTHON_VERSION < 3.0:
        s = unicodedata.normalize('NFKD', u)
        try:
            return s.encode('ascii')
        except UnicodeEncodeError:
            return s

    else:
        return str(u)


def load_code(fp, magic_int, code_objects={}):
    """
    marshal.load() written in Python. When the Python bytecode magic loaded is the
    same magic for the running Python interpreter, we can simply use the
    Python-supplied marshal.load().

    However we need to use this when versions are different since the internal
    code structures are different. Sigh.
    """
    global internObjects
    global internStrings
    internStrings = []
    internObjects = []
    seek_pos = fp.tell()
    b = ord(fp.read(1))
    save_ref = False
    if b & 128:
        save_ref = True
        internObjects.append(None)
        b = b & 127
    c = chr(b)
    if c == 'c' or magic_int in (39170, 39171) and c == 'C':
        fp.seek(seek_pos)
    else:
        raise TypeError("File %s doesn't smell like Python bytecode:\nexpecting code indicator 'c'; got '%s'" % (fp.name, c))
    code = load_code_internal(fp, magic_int, code_objects=code_objects)
    if save_ref:
        internObjects[0] = code
    return code


def load_code_type(fp, magic_int, bytes_for_s=False, code_objects={}):
    version = magic_int2float(magic_int)
    if version >= 2.3:
        co_argcount = unpack('<i', fp.read(4))[0]
    elif version >= 1.3:
        co_argcount = unpack('<h', fp.read(2))[0]
    else:
        co_argcount = 0
    if magic_int in (3412, 3413, 3422):
        co_posonlyargcount = unpack('<i', fp.read(4))[0]
    if version >= 3.8:
        co_posonlyargcount = 0
    else:
        co_posonlyargcount = None
    if version >= 3.0:
        kwonlyargcount = unpack('<i', fp.read(4))[0]
    else:
        kwonlyargcount = 0
    if version >= 2.3:
        co_nlocals = unpack('<i', fp.read(4))[0]
    elif version >= 1.3:
        co_nlocals = unpack('<h', fp.read(2))[0]
    else:
        co_nlocals = 0
    if version >= 2.3:
        co_stacksize = unpack('<i', fp.read(4))[0]
    elif version >= 1.5:
        co_stacksize = unpack('<h', fp.read(2))[0]
    else:
        co_stacksize = 0
    if version >= 2.3:
        co_flags = unpack('<i', fp.read(4))[0]
    elif version >= 1.3:
        co_flags = unpack('<h', fp.read(2))[0]
    else:
        co_flags = 0
    co_code = load_code_internal(fp, magic_int, bytes_for_s=True, code_objects=code_objects)
    co_consts = load_code_internal(fp, magic_int, code_objects=code_objects)
    co_names = load_code_internal(fp, magic_int, code_objects=code_objects)
    if version >= 1.3:
        co_varnames = load_code_internal(fp, magic_int, code_objects=code_objects)
    else:
        co_varnames = []
    if version >= 2.0:
        co_freevars = load_code_internal(fp, magic_int, code_objects=code_objects)
        co_cellvars = load_code_internal(fp, magic_int, code_objects=code_objects)
    else:
        co_freevars = tuple()
        co_cellvars = tuple()
    co_filename = load_code_internal(fp, magic_int, code_objects=code_objects)
    co_name = load_code_internal(fp, magic_int)
    if version >= 1.5:
        if version >= 2.3:
            co_firstlineno = unpack('<i', fp.read(4))[0]
        else:
            co_firstlineno = unpack('<h', fp.read(2))[0]
        co_lnotab = load_code_internal(fp, magic_int, code_objects=code_objects)
    else:
        co_firstlineno = -1
        co_lnotab = ''
    code = to_portable(co_argcount, co_posonlyargcount, kwonlyargcount, co_nlocals, co_stacksize, co_flags, co_code, co_consts, co_names, co_varnames, co_filename, co_name, co_firstlineno, co_lnotab, co_freevars, co_cellvars, version)
    code_objects[str(code)] = code
    return code


def r_ref_reserve(obj, flag):
    i = None
    if flag:
        i = len(internObjects)
        internObjects.append(obj)
    return (
     obj, i)


def r_ref_insert(obj, i):
    if i is not None:
        internObjects[i] = obj
    return obj


def r_ref(obj, flag):
    if flag:
        internObjects.append(obj)
    return obj


FLAG_REF = 128
UNMARSHAL_DISPATCH_TABLE = {}

def t_C_NULL(fp, flag=None, bytes_for_s=None, magic_int=None, code_objects=None):
    return


UNMARSHAL_DISPATCH_TABLE['0'] = t_C_NULL

def t_None(fp=None, flag=None, bytes_for_s=None, magic_int=None, code_objects=None):
    return


UNMARSHAL_DISPATCH_TABLE['N'] = t_None

def t_stopIteration(fp=None, flag=None, bytes_for_s=None, magic_int=None, code_objects=None):
    return StopIteration


UNMARSHAL_DISPATCH_TABLE['S'] = t_stopIteration

def t_Elipsis(fp=None, flag=None, bytes_for_s=None, magic_int=None, code_objects=None):
    return Ellipsis


UNMARSHAL_DISPATCH_TABLE['.'] = t_Elipsis

def t_False(fp=None, flag=None, bytes_for_s=None, magic_int=None, code_objects=None):
    return False


UNMARSHAL_DISPATCH_TABLE['F'] = t_False

def t_True(fp=None, flag=None, bytes_for_s=None, magic_int=None, code_objects=None):
    return True


UNMARSHAL_DISPATCH_TABLE['T'] = t_True

def t_int32(fp, flag, bytes_for_s=None, magic_int=None, code_objects=None):
    return r_ref(int(unpack('<i', fp.read(4))[0]), flag)


UNMARSHAL_DISPATCH_TABLE['i'] = t_int32

def t_long(fp, flag, bytes_for_s=None, magic_int=None, code_objects=None):
    n = unpack('<i', fp.read(4))[0]
    if n == 0:
        return long(0)
    size = abs(n)
    d = long(0)
    for j in range(0, size):
        md = int(unpack('<h', fp.read(2))[0])
        d += md << j * 15

    if n < 0:
        d = long(d * -1)
    return r_ref(d, flag)


UNMARSHAL_DISPATCH_TABLE['l'] = t_long

def t_int64(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    obj = unpack('<q', fp.read(8))[0]
    if save_ref:
        internObjects.append(obj)
    return obj


UNMARSHAL_DISPATCH_TABLE['I'] = t_int64

def t_float(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    strsize = unpack('B', fp.read(1))[0]
    s = fp.read(strsize)
    return r_ref(float(s), save_ref)


UNMARSHAL_DISPATCH_TABLE['f'] = t_float

def t_binary_float(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    return r_ref(float(unpack('<d', fp.read(8))[0]), save_ref)


UNMARSHAL_DISPATCH_TABLE['g'] = t_binary_float

def t_complex(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    if magic_int <= 62061:
        get_float = lambda : float(fp.read(unpack('B', fp.read(1))[0]))
    else:
        get_float = lambda : float(fp.read(unpack('<i', fp.read(4))[0]))
    real = get_float()
    imag = get_float()
    return r_ref(complex(real, imag), save_ref)


UNMARSHAL_DISPATCH_TABLE['x'] = t_complex

def t_binary_complex(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    real = unpack('<d', fp.read(8))[0]
    imag = unpack('<d', fp.read(8))[0]
    return r_ref(complex(real, imag), save_ref)


UNMARSHAL_DISPATCH_TABLE['y'] = t_binary_complex

def t_string(fp, save_ref, bytes_for_s, magic_int=None, code_objects=None):
    strsize = unpack('<i', fp.read(4))[0]
    s = fp.read(strsize)
    if not bytes_for_s:
        s = compat_str(s)
    return r_ref(s, save_ref)


UNMARSHAL_DISPATCH_TABLE['s'] = t_string

def t_ASCII_interned(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    strsize = unpack('<i', fp.read(4))[0]
    interned = compat_str(fp.read(strsize))
    internStrings.append(interned)
    return r_ref(interned, save_ref)


UNMARSHAL_DISPATCH_TABLE['A'] = t_ASCII_interned

def t_ASCII(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    strsize = unpack('<i', fp.read(4))[0]
    s = fp.read(strsize)
    s = compat_str(s)
    return r_ref(s, save_ref)


UNMARSHAL_DISPATCH_TABLE['a'] = t_ASCII

def t_short_ASCII(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    strsize = unpack('B', fp.read(1))[0]
    return r_ref(compat_str(fp.read(strsize)), save_ref)


UNMARSHAL_DISPATCH_TABLE['z'] = t_short_ASCII

def t_short_ASCII_interned(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    strsize = unpack('B', fp.read(1))[0]
    interned = compat_str(fp.read(strsize))
    internStrings.append(interned)
    return r_ref(interned, save_ref)


UNMARSHAL_DISPATCH_TABLE['Z'] = t_short_ASCII_interned

def t_interned(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    strsize = unpack('<i', fp.read(4))[0]
    interned = compat_str(fp.read(strsize))
    internStrings.append(interned)
    return r_ref(interned, save_ref)


UNMARSHAL_DISPATCH_TABLE['t'] = t_interned

def t_unicode(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    strsize = unpack('<i', fp.read(4))[0]
    unicodestring = fp.read(strsize)
    if PYTHON_VERSION == 3.2 and IS_PYPY:
        return r_ref(unicodestring.decode('utf-8', errors='ignore'), save_ref)
    else:
        return r_ref(unicodestring.decode('utf-8'), save_ref)


UNMARSHAL_DISPATCH_TABLE['u'] = t_unicode

def t_small_tuple(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    tuplesize = unpack('B', fp.read(1))[0]
    (ret, i) = r_ref_reserve(tuple(), save_ref)
    while tuplesize > 0:
        ret += (load_code_internal(fp, magic_int, code_objects=code_objects),)
        tuplesize -= 1

    return r_ref_insert(ret, i)


UNMARSHAL_DISPATCH_TABLE[')'] = t_small_tuple

def t_tuple(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    tuplesize = unpack('<i', fp.read(4))[0]
    ret = r_ref(tuple(), save_ref)
    while tuplesize > 0:
        ret += (load_code_internal(fp, magic_int, code_objects=code_objects),)
        tuplesize -= 1

    return ret


UNMARSHAL_DISPATCH_TABLE['('] = t_tuple

def t_list(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    n = unpack('<i', fp.read(4))[0]
    ret = r_ref(list(), save_ref)
    while n > 0:
        ret += (load_code_internal(fp, magic_int, code_objects=code_objects),)
        n -= 1

    return ret


UNMARSHAL_DISPATCH_TABLE['['] = t_list

def t_frozenset(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    setsize = unpack('<i', fp.read(4))[0]
    (ret, i) = r_ref_reserve(tuple(), save_ref)
    while setsize > 0:
        ret += (load_code_internal(fp, magic_int, code_objects=code_objects),)
        setsize -= 1

    return r_ref_insert(frozenset(ret), i)


UNMARSHAL_DISPATCH_TABLE['<'] = t_frozenset

def t_set(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    setsize = unpack('<i', fp.read(4))[0]
    (ret, i) = r_ref_reserve(tuple(), save_ref)
    while setsize > 0:
        ret += (load_code_internal(fp, magic_int, code_objects=code_objects),)
        setsize -= 1

    return r_ref_insert(set(ret), i)


UNMARSHAL_DISPATCH_TABLE['>'] = t_set

def t_int32(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    return r_ref(int(unpack('<i', fp.read(4))[0]), save_ref)


UNMARSHAL_DISPATCH_TABLE['i'] = t_int32

def t_dict(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    ret = r_ref(dict(), save_ref)
    raise KeyError(marshalType)


UNMARSHAL_DISPATCH_TABLE['{'] = t_dict

def t_python2_string_reference(fp, save_ref=None, bytes_for_s=None, magic_int=None, code_objects=None):
    refnum = unpack('<i', fp.read(4))[0]
    return internStrings[refnum]


UNMARSHAL_DISPATCH_TABLE['R'] = t_python2_string_reference

def t_code(fp, save_ref, bytes_for_s=None, magic_int=None, code_objects=None):
    code = load_code_type(fp, magic_int, bytes_for_s=False, code_objects=code_objects)
    if save_ref:
        internObjects.append(code)
    return code


UNMARSHAL_DISPATCH_TABLE['c'] = t_code
UNMARSHAL_DISPATCH_TABLE['C'] = t_code

def t_object_reference(fp, save_ref=None, bytes_for_s=None, magic_int=None, code_objects=None):
    refnum = unpack('<i', fp.read(4))[0]
    o = internObjects[refnum]
    return o


UNMARSHAL_DISPATCH_TABLE['r'] = t_object_reference

def t_unknown(fp, save_ref=None, bytes_for_s=None, magic_int=None, code_objects=None):
    raise KeyError(marshalType)


UNMARSHAL_DISPATCH_TABLE['?'] = t_unknown

def load_code_internal(fp, magic_int, bytes_for_s=False, code_objects={}):
    b1 = ord(fp.read(1))
    save_ref = False
    if b1 & FLAG_REF:
        save_ref = True
        b1 = b1 & FLAG_REF - 1
    marshalType = chr(b1)
    if marshalType in UNMARSHAL_DISPATCH_TABLE:
        return UNMARSHAL_DISPATCH_TABLE[marshalType](fp, save_ref, bytes_for_s, magic_int, code_objects)
    else:
        try:
            sys.stderr.write('Unknown type %i (hex %x) %c\n' % (ord(marshalType), hex(ord(marshalType)), marshalType))
        except TypeError:
            sys.stderr.write('Unknown type %i %c\n' % (ord(marshalType), marshalType))