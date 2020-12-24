# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/storage/eyes/virtualenv/pyte/lib/python3.5/site-packages/pyte/ops/for_.py
# Compiled at: 2016-04-19 12:03:31
# Size of source mod 2**32: 2055 bytes
"""
More complex than IF.
"""
import collections
from pyte import util, tokens
from pyte.superclasses import _PyteOp, _PyteAugmentedValidator

class FOR_LOOP(_PyteOp):

    def __init__(self, iterator, body: list):
        """
        Create a new FOR operator.

        Parameters:

            iterator: _PyteAugmentedValidator
                This should be a saved value that is iterable, i.e a saved list or something.

            body: list
                A list of instructions to execute, similarly to IF.
        """
        self.iterator = iterator
        self._body = list(util.flatten(body))

    def to_bytes(self, previous: bytes):
        bc = b''
        it_bc = util.generate_bytecode_from_obb(self.iterator, previous)
        bc += it_bc
        bc += util.generate_bytecode_from_obb(tokens.GET_ITER, b'')
        prev_len = len(previous) + len(bc)
        body_bc = b''
        for op in self._body:
            padded_bc = previous
            padded_bc += b'\x00\x00\x00'
            padded_bc += bc
            padded_bc += b'\x00\x00\x00'
            padded_bc += body_bc
            body_bc += util.generate_bytecode_from_obb(op, padded_bc)

        body_bc += util.generate_simple_call(tokens.JUMP_ABSOLUTE, prev_len + 3)
        body_bc += util.generate_bytecode_from_obb(tokens.POP_BLOCK, b'')
        body_bc = util.generate_simple_call(tokens.FOR_ITER, len(body_bc) - 1) + body_bc
        bc = util.generate_simple_call(tokens.SETUP_LOOP, prev_len + len(body_bc) - 6) + bc + body_bc
        return bc