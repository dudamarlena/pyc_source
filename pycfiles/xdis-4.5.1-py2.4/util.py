# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/util.py
# Compiled at: 2020-04-26 21:30:06
import types

def code2num(code, i):
    if isinstance(code, str):
        return ord(code[i])
    else:
        return code[i]


def num2code(num):
    return (
     num & 255, num >> 8)


COMPILER_FLAG_NAMES = {1: 'OPTIMIZED', 2: 'NEWLOCALS', 4: 'VARARGS', 8: 'VARKEYWORDS', 16: 'NESTED', 32: 'GENERATOR', 64: 'NOFREE', 128: 'COROUTINE', 256: 'ITERABLE_COROUTINE', 512: 'ASYNC_GENERATOR', 4096: 'GENERATOR_ALLOWED', 8192: 'FUTURE_DIVISION', 16384: 'ABSOLUTE_IMPORT', 32768: 'FUTURE_WITH_STATEMENT', 65536: 'FUTURE_PRINT_FUNCTION', 131072: 'FUTURE_UNICODE_LITERALS', 262144: 'FUTURE_BARRY_AS_DBFL'}
PYPY_COMPILER_FLAG_NAMES = {1048576: 'PYPY_KILL_DOCSTRING', 2097152: 'PYPY_YIELD_INSIDE_TRY', 1024: 'PYPY_ONLY_AST', 268435456: 'PYPY_ACCEPT_NULL_BYTES'}
COMPILER_FLAG_BIT = {}
for (v, k) in COMPILER_FLAG_NAMES.items():
    COMPILER_FLAG_BIT[k] = v

for (v, k) in COMPILER_FLAG_BIT.items():
    globals().update(dict({'CO_' + v: k}))

def co_flags_is_async(co_flags):
    """
    Return True iff co_flags indicates an async function.
    """
    return co_flags & (COMPILER_FLAG_BIT['COROUTINE'] | COMPILER_FLAG_BIT['ITERABLE_COROUTINE'] | COMPILER_FLAG_BIT['ASYNC_GENERATOR'])


def code_has_star_arg(code):
    """Return True iff
    the code object has a variable positional parameter (*args-like)"""
    return code.co_flags & 4 != 0


def code_has_star_star_arg(code):
    """Return True iff
    The code object has a variable keyword parameter (**kwargs-like)."""
    return code.co_flags & 8 != 0


def is_negative_zero(n):
    """Returns true if n is -0.0"""
    return n == 0.0


def better_repr(v):
    """Work around Python's unorthogonal and unhelpful repr() for primitive float
    and complex."""
    if isinstance(v, float):
        if str(v) in frozenset(['nan', '-nan', 'inf', '-inf']):
            return "float('%s')" % v
        elif is_negative_zero(v):
            return '-0.0'
        return repr(v)
    elif isinstance(v, complex):
        real = better_repr(v.real)
        imag = better_repr(v.imag)
        return 'complex(%s, %s)' % (real, imag)
    elif isinstance(v, tuple):
        if len(v) == 1:
            return '(%s,)' % better_repr(v[0])
        return '(%s)' % (', ').join((better_repr(i) for i in v))
    elif isinstance(v, list):
        l = better_repr(v)
        if len(v) == 1:
            return '[%s,]' % better_repr(v[0])
        return '[%s]' % (', ').join((better_repr(i) for i in v))
    else:
        return repr(v)