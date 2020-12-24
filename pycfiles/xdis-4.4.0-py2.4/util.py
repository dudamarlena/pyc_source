# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/util.py
# Compiled at: 2020-04-20 10:24:57
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

def pretty_flags(flags, is_pypy=False):
    """Return pretty representation of code flags."""
    names = []
    result = '0x%08x' % flags
    for i in range(32):
        flag = 1 << i
        if flags & flag:
            names.append(COMPILER_FLAG_NAMES.get(flag, hex(flag)))
            if is_pypy:
                names.append(PYPY_COMPILER_FLAG_NAMES.get(flag, hex(flag)))
            flags ^= flag
            if not flags:
                break
    else:
        names.append(hex(flags))

    names.reverse()
    return '%s (%s)' % (result, (' | ').join(names))


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


def format_code_info(co, version, name=None, is_pypy=False):
    if not name:
        name = co.co_name
    lines = []
    lines.append('# Method Name:       %s' % name)
    lines.append('# Filename:          %s' % co.co_filename)
    if version >= 1.3:
        lines.append('# Argument count:    %s' % co.co_argcount)
    if version >= 3.8 and hasattr(co, 'co_posonlyargcount'):
        lines.append('# Position-only argument count: %s' % co.co_posonlyargcount)
    if version >= 3.0 and hasattr(co, 'co_kwonlyargcount'):
        lines.append('# Keyword-only arguments: %s' % co.co_kwonlyargcount)
    pos_argc = co.co_argcount
    if version >= 1.3:
        lines.append('# Number of locals:  %s' % co.co_nlocals)
    if version >= 1.5:
        lines.append('# Stack size:        %s' % co.co_stacksize)
    if version >= 1.3:
        lines.append('# Flags:             %s' % pretty_flags(co.co_flags, is_pypy=is_pypy))
    if version >= 1.5:
        lines.append('# First Line:        %s' % co.co_firstlineno)
    if co.co_consts:
        lines.append('# Constants:')
        for (i, c) in enumerate(co.co_consts):
            lines.append('# %4d: %s' % (i, better_repr(c)))

    if co.co_names:
        lines.append('# Names:')
        for i_n in enumerate(co.co_names):
            lines.append('# %4d: %s' % i_n)

    if co.co_varnames:
        lines.append('# Varnames:')
        lines.append('#\t%s' % (', ').join(co.co_varnames))
    if pos_argc > 0:
        lines.append('# Positional arguments:')
        lines.append('#\t%s' % (', ').join(co.co_varnames[:pos_argc]))
    if len(co.co_varnames) > pos_argc:
        lines.append('# Local variables:')
        for (i, n) in enumerate(co.co_varnames[pos_argc:]):
            lines.append('# %4d: %s' % (pos_argc + i, n))

    if version > 2.0:
        if co.co_freevars:
            lines.append('# Free variables:')
            for i_n in enumerate(co.co_freevars):
                lines.append('# %4d: %s' % i_n)

        if co.co_cellvars:
            lines.append('# Cell variables:')
            for i_n in enumerate(co.co_cellvars):
                lines.append('# %4d: %s' % i_n)

    return ('\n').join(lines)


def _try_compile(source, name):
    """Attempts to compile the given source, first as an expression and
       then as a statement if the first approach fails.

       Utility function to accept strings in functions that otherwise
       expect code objects
    """
    try:
        c = compile(source, name, 'eval')
    except SyntaxError:
        c = compile(source, name, 'exec')

    return c


def get_code_object(x):
    """Helper to handle methods, functions, generators, strings and raw code objects"""
    if hasattr(x, '__func__'):
        x = x.__func__
    if hasattr(x, 'im_func'):
        x = x.im_func
    if hasattr(x, 'func_code'):
        x = x.func_code
    if hasattr(x, 'gi_code'):
        x = x.gi_code
    if hasattr(x, '__dict__'):
        items = x.__dict__.items()
        items.sort()
        for (name, x1) in items:
            if type(x1) in (types.MethodType, types.FunctionType, types.CodeType, types.ClassType):
                x = x1

    if hasattr(x, 'co_code'):
        return x
    if isinstance(x, str):
        x = _try_compile(x, '<disassembly>')
    raise TypeError("don't know how to disassemble %s objects" % type(x).__name__)


def code_info(x, version, is_pypy=False):
    """Formatted details of methods, functions, or code."""
    return format_code_info(get_code_object(x), version, is_pypy=is_pypy)


def show_code(co, version, file=None, is_pypy=False):
    """Print details of methods, functions, or code to *file*.

    If *file* is not provided, the output is printed on stdout.
    """
    if file is None:
        print code_info(co, version, is_pypy=is_pypy)
    else:
        file.write(code_info(co, version) + '\n')
    return