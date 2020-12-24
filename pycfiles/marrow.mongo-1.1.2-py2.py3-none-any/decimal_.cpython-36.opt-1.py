# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/core/field/decimal_.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 780 bytes
from __future__ import unicode_literals
from decimal import Decimal as dec, localcontext
from .number import Number
try:
    from bson.decimal128 import Decimal128, create_decimal128_context
except ImportError:
    Decimal = None
else:

    class Decimal(Number):
        __foreign__ = 'decimal'
        DECIMAL_CONTEXT = create_decimal128_context()

        def to_native(self, obj, name, value):
            if hasattr(value, 'to_decimal'):
                return value.to_decimal()
            else:
                return dec(value)

        def to_foreign(self, obj, name, value):
            if not isinstance(value, dec):
                with localcontext(self.DECIMAL_CONTEXT) as (ctx):
                    value = ctx.create_decimal(value)
            return Decimal128(value)