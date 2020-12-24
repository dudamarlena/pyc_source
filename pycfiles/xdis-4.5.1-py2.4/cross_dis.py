# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/cross_dis.py
# Compiled at: 2020-04-26 21:30:06
from xdis.util import COMPILER_FLAG_NAMES, PYPY_COMPILER_FLAG_NAMES, better_repr, code2num

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


def findlinestarts(code, dup_lines=False):
    """Find the offsets in a byte code which are start of lines in the source.

    Generate pairs (offset, lineno) as described in Python/compile.c.
    """
    lineno_table = code.co_lnotab
    if isinstance(lineno_table, dict):
        for (addr, lineno) in lineno_table.items():
            yield (
             addr, lineno)

    elif not isinstance(code.co_lnotab, str):
        byte_increments = list(code.co_lnotab[0::2])
        line_increments = list(code.co_lnotab[1::2])
    else:
        byte_increments = [ ord(c) for c in code.co_lnotab[0::2] ]
        line_increments = [ ord(c) for c in code.co_lnotab[1::2] ]
    lastlineno = None
    lineno = code.co_firstlineno
    offset = 0
    for (byte_incr, line_incr) in zip(byte_increments, line_increments):
        if byte_incr:
            if (lineno != lastlineno or dup_lines) and 0 < byte_incr < 255:
                yield (
                 offset, lineno)
                lastlineno = lineno
            offset += byte_incr
        lineno += line_incr

    if (lineno != lastlineno or dup_lines) and 0 < byte_incr < 255:
        yield (
         offset, lineno)
    return


def code_info(x, version, is_pypy=False):
    """Formatted details of methods, functions, or code."""
    return format_code_info(get_code_object(x), version, is_pypy=is_pypy)


def get_code_object(x):
    """Helper to handle methods, functions, generators, strings and raw code objects"""
    if hasattr(x, '__func__'):
        x = x.__func__
    if hasattr(x, '__code__'):
        x = x.__code__
    elif hasattr(x, 'func_code'):
        x = x.__code__
    elif hasattr(x, 'gi_code'):
        x = x.gi_code
    elif hasattr(x, 'ag_code'):
        x = x.ag_code
    elif hasattr(x, 'cr_code'):
        x = x.cr_code
    if isinstance(x, str):
        x = _try_compile(x, '<disassembly>')
    if hasattr(x, 'co_code'):
        return x
    raise TypeError("don't know how to disassemble %s objects" % type(x).__name__)


def get_jump_targets(code, opc):
    """Returns a list of instruction offsets in the supplied bytecode
    which are the targets of some sort of jump instruction.
    """
    offsets = []
    for (offset, op, arg) in unpack_opargs_bytecode(code, opc):
        if arg is not None:
            jump_offset = -1
            if op in opc.JREL_OPS:
                op_len = op_size(op, opc)
                jump_offset = offset + op_len + arg
            elif op in opc.JABS_OPS:
                jump_offset = arg
            if jump_offset >= 0:
                if jump_offset not in offsets:
                    offsets.append(jump_offset)

    return offsets


findlabels = get_jump_targets

def instruction_size(op, opc):
    """For a given opcode, `op`, in opcode module `opc`,
    return the size, in bytes, of an `op` instruction.

    This is the size of the opcode (1 byte) and any operand it has. In
    Python before version 3.6 this will be either 1 or 3 bytes.  In
    Python 3.6 or later, it is 2 bytes or a "word"."""
    if op < opc.HAVE_ARGUMENT:
        if opc.version >= 3.6:
            return 2
        else:
            return 1
    elif opc.version >= 3.6:
        return 2
    else:
        return 3


op_size = instruction_size

def show_code(co, version, file=None, is_pypy=False):
    """Print details of methods, functions, or code to *file*.

    If *file* is not provided, the output is printed on stdout.
    """
    if file is None:
        print code_info(co, version, is_pypy=is_pypy)
    else:
        file.write(code_info(co, version) + '\n')
    return


def op_has_argument(op, opc):
    return op >= opc.HAVE_ARGUMENT


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


def extended_arg_val(opc, val):
    return val << opc.EXTENDED_ARG_SHIFT


def unpack_opargs_bytecode(code, opc):
    extended_arg = 0
    try:
        n = len(code)
    except TypeError:
        code = code.co_code
        n = len(code)

    offset = 0
    while offset < n:
        prev_offset = offset
        op = code2num(code, offset)
        offset += 1
        if op_has_argument(op, opc):
            arg = code2num(code, offset) | extended_arg
            if op == opc.EXTENDED_ARG:
                extended_arg = arg << opc.EXTENDED_ARG_SHIFT
            else:
                extended_arg = 0
            offset += 2
        else:
            arg = None
        yield (
         prev_offset, op, arg)

    return


def get_jump_target_maps(code, opc):
    """Returns a dictionary where the key is an offset and the values are
    a list of instruction offsets which can get run before that
    instruction. This includes jump instructions as well as non-jump
    instructions. Therefore, the keys of the dictionary are reachable
    instructions. The values of the dictionary may be useful in control-flow
    analysis.
    """
    offset2prev = {}
    prev_offset = -1
    for (offset, op, arg) in unpack_opargs_bytecode(code, opc):
        if prev_offset >= 0:
            prev_list = offset2prev.get(offset, [])
            prev_list.append(prev_offset)
            offset2prev[offset] = prev_list
        if op in opc.NOFOLLOW:
            prev_offset = -1
        else:
            prev_offset = offset
        if arg is not None:
            jump_offset = -1
            if op in opc.JREL_OPS:
                op_len = op_size(op, opc)
                jump_offset = offset + op_len + arg
            elif op in opc.JABS_OPS:
                jump_offset = arg
            if jump_offset >= 0:
                prev_list = offset2prev.get(jump_offset, [])
                prev_list.append(offset)
                offset2prev[jump_offset] = prev_list

    return offset2prev


def xstack_effect(opcode, opc, oparg=None, jump=None):
    """Compute the stack effect of opcode with argument oparg, using
    oppush and oppop tables in opc.

    If the code has a jump target and jump is True, stack_effect()
    will return the stack effect of jumping. If jump is False, it will
    return the stack effect of not jumping. And if jump is None
    (default), it will return the maximal stack effect of both cases.
    """
    pop, push = opc.oppop[opcode], opc.oppush[opcode]
    opname = opc.opname[opcode]
    if opname in ('BUILD_MAP', ):
        if opc.version >= 3.5:
            return 1 - 2 * oparg
    elif opname in ('UNPACK_SEQUENCE', 'UNPACK_EX') and opc.version >= 3.0:
        return push + oparg
    elif opname in 'BUILD_SLICE' and opc.version <= 2.7:
        if oparg == 3:
            return -2
        else:
            return -1
    elif opname == 'MAKE_FUNCTION':
        if opc.version >= 3.5:
            if 0 <= oparg <= 10:
                if opc.version == 3.5:
                    return [
                     -1, -2, -3, -3, -2, -3, -3, -4, -2, -3, -3, -4][oparg]
                elif opc.version >= 3.6:
                    return [
                     -1, -2, -2, -3, -2, -3, -3, -4, -2, -3, -3, -4][oparg]
            else:
                return
    elif opname == 'CALL_FUNCTION_EX':
        if opc.version >= 3.5:
            if 0 <= oparg <= 10:
                return [
                 -1, -2, -1][oparg]
            else:
                return
    if push >= 0 and pop >= 0:
        return push - pop
    elif pop < 0:
        if opcode in opc.VARGS_OPS:
            return push - oparg + (pop + 1)
        elif opcode in opc.NARGS_OPS:
            return -oparg + pop + push
    return -100


def check_stack_effect():
    import dis
    from xdis import IS_PYPY
    from xdis.op_imports import get_opcode_module
    if IS_PYPY:
        variant = 'pypy'
    else:
        variant = ''
    opc = get_opcode_module(None, variant)
    for (opname, opcode) in opc.opmap.items():
        if opname in ('EXTENDED_ARG', 'NOP'):
            continue
        xdis_args = [
         opcode, opc]
        dis_args = [opcode]
        if op_has_argument(opcode, opc):
            xdis_args.append(0)
            dis_args.append(0)
        if PYTHON_VERSION > 3.7 and opcode in opc.CONDITION_OPS and opname not in ('JUMP_IF_FALSE_OR_POP',
                                                                                   'JUMP_IF_TRUE_OR_POP',
                                                                                   'POP_JUMP_IF_FALSE',
                                                                                   'POP_JUMP_IF_TRUE',
                                                                                   'SETUP_FINALLY'):
            xdis_args.append(0)
            dis_args.append(0)
        effect = xstack_effect(*xdis_args)
        check_effect = dis.stack_effect(*dis_args)
        if effect == -100:
            print '%d (%s) needs adjusting; should be: should have effect %d' % (opcode, opname, check_effect)
        elif check_effect == effect:
            pass
        else:
            print '%d (%s) not okay; effect %d vs %d' % (opcode, opname, effect, check_effect)

    return


if __name__ == '__main__':
    from xdis import PYTHON_VERSION
    if PYTHON_VERSION >= 3.4:
        check_stack_effect()