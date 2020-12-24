# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/coverage/coverage/bytecode.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 2036 bytes
"""Bytecode manipulation for coverage.py"""
import opcode, types
from coverage.backward import byte_to_int

class ByteCode(object):
    __doc__ = 'A single bytecode.'

    def __init__(self):
        self.offset = -1
        self.op = -1
        self.arg = -1
        self.next_offset = -1
        self.jump_to = -1


class ByteCodes(object):
    __doc__ = 'Iterator over byte codes in `code`.\n\n    Returns `ByteCode` objects.\n\n    '

    def __init__(self, code):
        self.code = code

    def __getitem__(self, i):
        return byte_to_int(self.code[i])

    def __iter__(self):
        offset = 0
        while offset < len(self.code):
            bc = ByteCode()
            bc.op = self[offset]
            bc.offset = offset
            next_offset = offset + 1
            if bc.op >= opcode.HAVE_ARGUMENT:
                bc.arg = self[(offset + 1)] + 256 * self[(offset + 2)]
                next_offset += 2
                label = -1
                if bc.op in opcode.hasjrel:
                    label = next_offset + bc.arg
                else:
                    if bc.op in opcode.hasjabs:
                        label = bc.arg
                bc.jump_to = label
            bc.next_offset = offset = next_offset
            yield bc


class CodeObjects(object):
    __doc__ = 'Iterate over all the code objects in `code`.'

    def __init__(self, code):
        self.stack = [code]

    def __iter__(self):
        while self.stack:
            code = self.stack.pop()
            for c in code.co_consts:
                if isinstance(c, types.CodeType):
                    self.stack.append(c)

            yield code