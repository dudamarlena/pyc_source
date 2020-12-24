# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/scanner38.py
# Compiled at: 2020-04-20 23:02:15
"""
Python 3.8 bytecode decompiler scanner.

Does some additional massaging of xdis-disassembled instructions to
make things easier for decompilation.

This sets up opcodes Python's 3.8 and calls a generalized
scanner routine for Python 3.7 and up.
"""
from uncompyle6.scanners.tok import off2int
from uncompyle6.scanners.scanner37 import Scanner37
from uncompyle6.scanners.scanner37base import Scanner37Base
from xdis.opcodes import opcode_38 as opc
JUMP_OPs = opc.JUMP_OPS

class Scanner38(Scanner37):
    __module__ = __name__

    def __init__(self, show_asm=None):
        Scanner37Base.__init__(self, 3.8, show_asm)
        self.debug = False

    def ingest(self, co, classname=None, code_objects={}, show_asm=None):
        (tokens, customize) = super(Scanner38, self).ingest(co, classname, code_objects, show_asm)
        jump_back_targets = {}
        for token in tokens:
            if token.kind == 'JUMP_BACK':
                jump_back_targets[token.attr] = token.offset

        if self.debug and jump_back_targets:
            print jump_back_targets
        loop_ends = []
        next_end = tokens[(len(tokens) - 1)].off2int() + 10
        for (i, token) in enumerate(tokens):
            opname = token.kind
            offset = token.offset
            if offset == next_end:
                loop_ends.pop()
                if self.debug:
                    print '%sremove loop offset %s' % (' ' * len(loop_ends), offset)
                if len(loop_ends):
                    next_end = loop_ends[(-1)]
                else:
                    next_end = tokens[(len(tokens) - 1)].off2int() + 10
            if offset in jump_back_targets:
                next_end = off2int(jump_back_targets[offset], prefer_last=False)
                if self.debug:
                    print '%sadding loop offset %s ending at %s' % ('  ' * len(loop_ends), offset, next_end)
                loop_ends.append(next_end)
            if opname in ('JUMP_FORWARD', 'JUMP_ABSOLUTE') and len(loop_ends):
                jump_target = token.attr
                if opname == 'JUMP_ABSOLUTE' and jump_target <= next_end:
                    continue
                if i + 1 < len(tokens) and tokens[(i + 1)] == 'JUMP_BACK':
                    jump_back_index = i + 1
                else:
                    jump_back_index = self.offset2tok_index[jump_target] - 1
                    while tokens[jump_back_index].kind.startswith('COME_FROM_'):
                        jump_back_index -= 1

                jump_back_token = tokens[jump_back_index]
                break_loop = token.linestart and jump_back_token != 'JUMP_BACK'
                if break_loop or jump_back_token == 'JUMP_BACK' and jump_back_token.attr < token.off2int():
                    token.kind = 'BREAK_LOOP'

        return (
         tokens, customize)


if __name__ == '__main__':
    from uncompyle6 import PYTHON_VERSION
    if PYTHON_VERSION == 3.8:
        import inspect
        co = inspect.currentframe().f_code
        (tokens, customize) = Scanner38().ingest(co)
        for t in tokens:
            print t.format()

    else:
        print 'Need to be Python 3.8 to demo; I am %s.' % PYTHON_VERSION