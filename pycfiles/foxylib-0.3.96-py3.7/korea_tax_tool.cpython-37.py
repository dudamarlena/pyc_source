# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/finance/tax/korea/korea_tax_tool.py
# Compiled at: 2020-01-21 23:08:22
# Size of source mod 2**32: 315 bytes
from decimal import Decimal

class KoreaTaxTool:

    class Value:
        VAT_RATIO = Decimal('0.10')

    V = Value

    @classmethod
    def charged2vat_removed(cls, v):
        return v / (1 + cls.V.VAT_RATIO)

    @classmethod
    def price2vat_added(cls, v):
        return (v * (1 + cls.V.VAT_RATIO)).normalize()