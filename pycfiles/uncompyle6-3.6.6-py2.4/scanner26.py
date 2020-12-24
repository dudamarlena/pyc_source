# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/scanner26.py
# Compiled at: 2020-04-18 17:55:36
"""
Python 2.6 bytecode scanner

This overlaps Python's 2.6's dis module, but it can be run from Python 3 and
other versions of Python. Also, we save token information for later
use in deparsing.
"""
import sys
from uncompyle6 import PYTHON3
if PYTHON3:
    intern = sys.intern
import uncompyle6.scanners.scanner2 as scan
from uncompyle6.scanner import L65536
from xdis.opcodes import opcode_26
from xdis.bytecode import _get_const_info
from uncompyle6.scanner import Token
JUMP_OPS = opcode_26.JUMP_OPS

class Scanner26(scan.Scanner2):
    __module__ = __name__

    def __init__(self, show_asm=False):
        super(Scanner26, self).__init__(2.6, show_asm)
        self.setup_ops = frozenset([self.opc.SETUP_EXCEPT, self.opc.SETUP_FINALLY])

    def ingest(self, co, classname=None, code_objects={}, show_asm=None):
        """
        Pick out tokens from an uncompyle6 code object, and transform them,
        returning a list of uncompyle6 'Token's.

        The transformations are made to assist the deparsing grammar.
        Specificially:
           -  various types of LOAD_CONST's are categorized in terms of what they load
           -  COME_FROM instructions are added to assist parsing control structures
           -  MAKE_FUNCTION and FUNCTION_CALLS append the number of positional arguments

        Also, when we encounter certain tokens, we add them to a set which will cause custom
        grammar rules. Specifically, variable arg tokens like MAKE_FUNCTION or BUILD_LIST
        cause specific rules for the specific number of arguments they take.
        """
        if not show_asm:
            show_asm = self.show_asm
        bytecode = self.build_instructions(co)
        if show_asm in ('both', 'before'):
            for instr in bytecode.get_instructions(co):
                print instr.disassemble()

        tokens = []
        customize = {}
        if self.is_pypy:
            customize['PyPy'] = 1
        codelen = len(self.code)
        (free, names, varnames) = self.unmangle_code_names(co, classname)
        self.names = names
        self.load_asserts = set()
        for i in self.op_range(0, codelen):
            if self.code[i] == self.opc.JUMP_IF_TRUE and i + 4 < codelen and self.code[(i + 3)] == self.opc.POP_TOP and self.code[(i + 4)] == self.opc.LOAD_GLOBAL:
                if names[self.get_argument(i + 4)] == 'AssertionError':
                    self.load_asserts.add(i + 4)

        jump_targets = self.find_jump_targets(show_asm)
        last_stmt = self.next_stmt[0]
        i = self.next_stmt[last_stmt]
        replace = {}
        while i < codelen - 1:
            if self.lines[last_stmt].next > i:
                if self.code[last_stmt] == self.opc.PRINT_ITEM:
                    if self.code[i] == self.opc.PRINT_ITEM:
                        replace[i] = 'PRINT_ITEM_CONT'
                    elif self.code[i] == self.opc.PRINT_NEWLINE:
                        replace[i] = 'PRINT_NEWLINE_CONT'
            last_stmt = i
            i = self.next_stmt[i]

        extended_arg = 0
        for offset in self.op_range(0, codelen):
            op = self.code[offset]
            op_name = self.opname[op]
            oparg = None
            pattr = None
            if offset in jump_targets:
                jump_idx = 0
                last_jump_offset = -1
                for jump_offset in sorted(jump_targets[offset], reverse=True):
                    if jump_offset != last_jump_offset:
                        tokens.append(Token('COME_FROM', jump_offset, repr(jump_offset), offset='%s_%d' % (offset, jump_idx), has_arg=True))
                        jump_idx += 1
                        last_jump_offset = jump_offset

            if offset in self.thens:
                tokens.append(Token('THEN', None, self.thens[offset], offset='%s_0' % offset, has_arg=True))
            has_arg = op >= self.opc.HAVE_ARGUMENT
            if has_arg:
                oparg = self.get_argument(offset) + extended_arg
                extended_arg = 0
                if op == self.opc.EXTENDED_ARG:
                    extended_arg = oparg * L65536
                    continue
                if op in self.opc.CONST_OPS:
                    const = co.co_consts[oparg]
                    if hasattr(const, 'co_name'):
                        oparg = const
                        if const.co_name == '<lambda>':
                            assert op_name == 'LOAD_CONST'
                            op_name = 'LOAD_LAMBDA'
                        elif const.co_name == self.genexpr_name:
                            op_name = 'LOAD_GENEXPR'
                        elif const.co_name == '<dictcomp>':
                            op_name = 'LOAD_DICTCOMP'
                        elif const.co_name == '<setcomp>':
                            op_name = 'LOAD_SETCOMP'
                        else:
                            op_name = 'LOAD_CODE'
                        pattr = '<code_object ' + const.co_name + '>'
                    else:
                        if oparg < len(co.co_consts):
                            (argval, _) = _get_const_info(oparg, co.co_consts)
                        pattr = const
                elif op in self.opc.NAME_OPS:
                    pattr = names[oparg]
                elif op in self.opc.JREL_OPS:
                    pattr = repr(offset + 3 + oparg)
                    if op == self.opc.JUMP_FORWARD:
                        target = self.get_target(offset)
                        if len(tokens) and tokens[(-1)].kind == 'JUMP_BACK':
                            tokens[(-1)].kind = intern('CONTINUE')
                elif op in self.opc.JABS_OPS:
                    pattr = repr(oparg)
                elif op in self.opc.LOCAL_OPS:
                    pattr = varnames[oparg]
                elif op in self.opc.COMPARE_OPS:
                    pattr = self.opc.cmp_op[oparg]
                elif op in self.opc.FREE_OPS:
                    pattr = free[oparg]
            if op in self.varargs_ops:
                if self.version >= 2.5 and op == self.opc.BUILD_TUPLE and self.code[self.prev[offset]] == self.opc.LOAD_CLOSURE:
                    continue
                else:
                    op_name = '%s_%d' % (op_name, oparg)
                    customize[op_name] = oparg
            elif self.version > 2.0 and op == self.opc.CONTINUE_LOOP:
                customize[op_name] = 0
            elif op_name in ('\n                 CONTINUE_LOOP EXEC_STMT LOAD_LISTCOMP LOAD_SETCOMP\n                  ').split():
                customize[op_name] = 0
            elif op == self.opc.JUMP_ABSOLUTE:
                target = self.get_target(offset)
                if target <= offset:
                    op_name = 'JUMP_BACK'
                    if offset in self.stmts:
                        if self.code[(offset + 3)] not in (self.opc.END_FINALLY, self.opc.POP_BLOCK) and (offset in self.linestarts and tokens[(-1)].kind == 'JUMP_BACK' or offset not in self.not_continue):
                            op_name = 'CONTINUE'
                    elif tokens[(-1)].kind == 'JUMP_BACK':
                        tokens[(-1)].kind = intern('CONTINUE')
            elif op == self.opc.LOAD_GLOBAL:
                if offset in self.load_asserts:
                    op_name = 'LOAD_ASSERT'
            elif op == self.opc.RETURN_VALUE:
                if offset in self.return_end_ifs:
                    op_name = 'RETURN_END_IF'
            linestart = self.linestarts.get(offset, None)
            if offset not in replace:
                tokens.append(Token(op_name, oparg, pattr, offset, linestart, op, has_arg, self.opc))
            else:
                tokens.append(Token(replace[offset], oparg, pattr, offset, linestart, op, has_arg, self.opc))

        if show_asm in ('both', 'after'):
            for t in tokens:
                print t.format(line_prefix='')

            print ()
        return (
         tokens, customize)


if __name__ == '__main__':
    from uncompyle6 import PYTHON_VERSION
    if PYTHON_VERSION == 2.6:
        import inspect
        co = inspect.currentframe().f_code
        (tokens, customize) = Scanner26(show_asm=True).ingest(co)
    else:
        print 'Need to be Python 2.6 to demo; I am %s.' % PYTHON_VERSION