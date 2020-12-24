# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/storage/eyes/virtualenv/pyte/lib/python3.5/site-packages/pyte/ops/call.py
# Compiled at: 2016-04-17 12:10:26
# Size of source mod 2**32: 2917 bytes
"""
File for CALL_FUNCTION.

This does a bit of optimizing out, and makes it nicer to run than manually LOAD_ing the calls.
"""
from pyte.exc import ValidationError
from pyte.superclasses import _PyteOp, _PyteAugmentedValidator
from pyte import util, tokens

class CALL_FUNCTION(_PyteOp):
    __doc__ = '\n    CALL_FUNCTION.\n\n    This function takes one or more indexes as arguments.\n    '

    def __init__(self, function, *args, store_return=None):
        self.fun = function
        self.args = args
        if store_return:
            self._store_list = store_return
        else:
            self._store_list = False

    def to_bytes(self, previois) -> bytes:
        arg_count = len(self.args)
        bc = b''
        if not isinstance(self.fun, _PyteAugmentedValidator):
            raise ValidationError('Function to call must be inside names')
        self.fun.validate()
        f_index = self.fun.index
        l_g = util.generate_load_global(f_index)
        bc += l_g
        for arg in self.args:
            try:
                assert isinstance(arg, _PyteAugmentedValidator)
            except AssertionError:
                raise ValidationError('CALL_FUNCTION args must be validated') from None

            arg.validate()
            if arg.list_name == 'consts':
                bc += util.generate_load_const(arg.index)
            else:
                if arg.list_name == 'varnames':
                    bc += util.generate_load_fast(arg.index)
                else:
                    raise ValidationError('Could not determine call to use with list type {}'.format(arg.list_name))

        bc += tokens.CALL_FUNCTION.to_bytes(1, byteorder='little')
        bc += arg_count.to_bytes(1, byteorder='little')
        bc += b'\x00'
        if not self._store_list:
            bc += tokens.POP_TOP.to_bytes(1, byteorder='little')
        else:
            bc += util.generate_simple_call(tokens.STORE_FAST, self._store_list.index)
        return bc