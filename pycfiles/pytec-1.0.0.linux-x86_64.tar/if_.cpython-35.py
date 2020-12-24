# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/storage/eyes/virtualenv/pyte/lib/python3.5/site-packages/pyte/ops/if_.py
# Compiled at: 2016-04-17 09:32:49
# Size of source mod 2**32: 3176 bytes
"""
IF operands.
This is horrible code, that detects jumps.
You have been warned.
"""
from pyte import exc, tokens
from pyte.compiler import _compile_bc
from pyte.superclasses import _PyteOp, _PyteAugmentedValidator
from pyte.util import generate_simple_call

class IF(_PyteOp):
    __doc__ = "\n    An IF operator is Pyte's implementation of the `if elif else` syntax.\n\n    This uses a slightly convoluted syntax to define the IF/ELSE, and set up the appropriate jumps.\n    "

    def __init__(self, conditions: list, body: list):
        """
        Create a new IF operator.

        Parameters:

            conditions: list
                Conditions is a list of conditions to check the IF statement for.
                These can be wrapped in a :class:`pyte.superclasses.PyteOr`/:class:`pyte.superclasses.PyteAnd` if you
                wish to have multiple conditions for one block.

                Conditions can be created using the standard truth operators (<, >, >=, <=, ==, !=). If there is only
                one condition to check (i.e a truthy check) that will be evaluated to generate the bytecode.

            body: list
                This should be a LIST OF LISTS. There should be as many lists as there are conditions to check. If
                there are not, a CompileError will be raised.

                These lists are standard lists of instructions for the Pyte compiler.
        """
        self.conditions = conditions
        self.body = body

    def to_bytes(self, previous: bytes):
        """
        Complex code ahead. Comments have been added in as needed.
        """
        if len(self.conditions) != len(self.body):
            raise exc.CompileError('Conditions and body length mismatch!')
        bc = b''
        prev_len = len(previous)
        for condition, body in zip(self.conditions, self.body):
            cond_bytecode = condition.to_bytecode(previous)
            bc += cond_bytecode
            body_bc = _compile_bc(body)
            bdyl = len(body_bc)
            gen_len = prev_len + len(cond_bytecode) + bdyl + 3
            bc += generate_simple_call(tokens.POP_JUMP_IF_FALSE, gen_len)
            bc += body_bc
            prev_len = len(previous) + len(bc)

        return bc