# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/storage/eyes/virtualenv/pyte/lib/python3.5/site-packages/pyte/compiler.py
# Compiled at: 2016-04-20 01:43:49
# Size of source mod 2**32: 5531 bytes
"""
Compiles python bytecode using `types.FunctionType`.
"""
import dis, sys, warnings
from pyte import tokens
from pyte import util
from pyte.superclasses import _PyteOp, _PyteAugmentedComparator
from pyte.exc import CompileError
import inspect, types

def _compile_bc(code: list) -> bytes:
    """
    Compiles Pyte objects into a bytecode string.
    """
    bc = b''
    for i, op in enumerate(code):
        try:
            if isinstance(op, _PyteOp) or isinstance(op, _PyteAugmentedComparator):
                bc_op = op.to_bytes(bc)
            else:
                if isinstance(op, int):
                    bc_op = op.to_bytes(1, byteorder='little')
                else:
                    if isinstance(op, bytes):
                        bc_op = op
                    else:
                        raise CompileError('Could not compile code of type {}'.format(type(op)))
            bc += bc_op
        except Exception as e:
            print('Fatal compiliation error on operator {i} ({op}).'.format(i=i, op=op))
            raise e

    return bc


def _simulate_stack(code: list) -> int:
    """
    Simulates the actions of the stack, to check safety.

    This returns the maximum needed stack.
    """
    max_stack = 0
    curr_stack = 0

    def _check_stack(ins):
        if curr_stack < 0:
            raise CompileError('Stack turned negative on instruction: {}'.format(ins))
        if curr_stack > max_stack:
            return curr_stack

    for instruction in code:
        assert isinstance(instruction, dis.Instruction)
        if instruction.arg is not None:
            effect = dis.stack_effect(instruction.opcode, instruction.arg)
        else:
            effect = dis.stack_effect(instruction.opcode)
        curr_stack += effect
        _should_new_stack = _check_stack(instruction)
        if _should_new_stack:
            max_stack = _should_new_stack

    return max_stack


def _optimize_warn_pass(bc: list):
    previous = None
    for op in bc:
        assert isinstance(op, dis.Instruction)
        if previous is None:
            previous = op
            continue
            if previous.opname == 'STORE_FAST' and op.opname == 'LOAD_FAST' and op.arg == previous.arg:
                warnings.warn('STORE_FAST call followed by LOAD_FAST call has no effect')


def compile(code: list, consts: list, names: list, varnames: list, func_name: str='<unknown, compiled>',
            arg_count=0):
    """
    Compiles a set of bytecode instructions into a working function, using Python's bytecode compiler.

    Parameters:
        code: list
            This represents a list of bytecode instructions.
            These should be Pyte-validated objects, to prevent segfaults on running the code.

        consts: list
            A list of constants.
            These constants can be any objects. They will not be validated.

        names: list
            A list of global names.
            These will be used with LOAD_GLOBAL, and functions.

        varnames: list
            A list of `parameter arguments`.

        func_name: str
            The name of the function.

        arg_count: int
            The number of arguments to have. This must be less than or equal to the number of varnames.
    """
    varnames = tuple(varnames)
    consts = tuple(consts)
    names = tuple(names)
    code = util.flatten(code)
    if arg_count > len(varnames):
        raise CompileError('arg_count > len(varnames)')
    bc = _compile_bc(code)
    if bc[(-1)] != tokens.RETURN_VALUE:
        raise CompileError("No default RETURN_VALUE. Add a `pyte.tokens.RETURN_VALUE` to the end of your bytecode if you don't need one.")
    flags = 67
    frame_data = inspect.stack()[1]
    if sys.version_info[0:2] > (3, 3):
        stack_size = _simulate_stack(dis._get_instructions_bytes(bc, constants=consts, names=names, varnames=varnames))
    else:
        warnings.warn('Cannot check stack for safety.')
        stack_size = 99
    _optimize_warn_pass(dis._get_instructions_bytes(bc, constants=consts, names=names, varnames=varnames))
    obb = types.CodeType(arg_count, 0, len(varnames), stack_size, flags, bc, consts, names, varnames, frame_data[1], func_name, frame_data[2], b'', (), ())
    f_globals = frame_data[0].f_globals
    f = types.FunctionType(obb, f_globals)
    f.__name__ = func_name
    return f