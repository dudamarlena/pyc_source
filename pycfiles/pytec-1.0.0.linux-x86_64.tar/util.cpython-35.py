# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/storage/eyes/virtualenv/pyte/lib/python3.5/site-packages/pyte/util.py
# Compiled at: 2016-04-20 01:32:41
# Size of source mod 2**32: 2533 bytes
"""
Miscellaneous utilities.
"""
import collections, dis, sys
from . import tokens
import pyte

def generate_simple_call(opcode, index):
    bs = b''
    bs += opcode.to_bytes(1, byteorder='little')
    if isinstance(index, int):
        bs += index.to_bytes(2, byteorder='little')
    else:
        bs += index
    return bs


def generate_bytecode_from_obb(obb: object, previous: bytes) -> bytes:
    if isinstance(obb, pyte.superclasses._PyteOp):
        return obb.to_bytes(previous)
    if isinstance(obb, (pyte.superclasses._PyteAugmentedComparator,
     pyte.superclasses._PyteAugmentedValidator._FakeMathematicalOP)):
        return obb.to_bytes(previous)
    if isinstance(obb, pyte.superclasses._PyteAugmentedValidator):
        obb.validate()
        return obb.to_load()
    if isinstance(obb, int):
        return obb.to_bytes((obb.bit_length() + 7) // 8, byteorder='little') or b''
    if isinstance(obb, bytes):
        return obb
    raise TypeError('`{}` was not a valid bytecode-encodable item'.format(obb))


def generate_load_global(index) -> bytes:
    return generate_simple_call(tokens.LOAD_GLOBAL, index)


def generate_load_fast(index) -> bytes:
    """
    Generates a LOAD_FAST operation.
    """
    return generate_simple_call(tokens.LOAD_FAST, index)


def generate_load_const(index) -> bytes:
    return generate_simple_call(tokens.LOAD_CONST, index)


def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            for sub in flatten(el):
                yield sub

        else:
            yield el


def _get_name_info(name_index, name_list):
    """Helper to get optional details about named references

       Returns the dereferenced name as both value and repr if the name
       list is defined.
       Otherwise returns the name index and its repr().
    """
    argval = name_index
    if name_list is not None:
        try:
            argval = name_list[name_index]
        except IndexError:
            return ('(unknown)', '(unknown)')

        argrepr = argval
    else:
        argrepr = repr(argval)
    return (
     argval, argrepr)


dis._get_name_info = _get_name_info
if sys.version_info[0:2] < (3, 4):
    from pyte import backports
    backports.apply()