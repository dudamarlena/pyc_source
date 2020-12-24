# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/storage/eyes/virtualenv/pyte/lib/python3.5/site-packages/pyte/ops/store.py
# Compiled at: 2016-04-17 06:26:14
# Size of source mod 2**32: 836 bytes
"""
STORE_FAST operation.
"""
from pyte import util, tokens
from pyte.exc import CompileError, ValidationError
from pyte.superclasses import _PyteOp, _PyteAugmentedValidator

class STORE_FAST(_PyteOp):
    __doc__ = '\n    This represents a STORE_FAST operation.\n    '

    def to_bytes(self, previous):
        try:
            arg = self.args[0]
        except IndexError:
            raise CompileError('No varname was passed to store in.') from None

        try:
            assert isinstance(arg, _PyteAugmentedValidator)
        except AssertionError:
            raise ValidationError('Passed in varname was not validated')

        arg.validate()
        opp = util.generate_simple_call(tokens.STORE_FAST, arg.index)
        return opp