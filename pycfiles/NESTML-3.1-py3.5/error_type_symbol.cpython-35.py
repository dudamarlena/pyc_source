# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/symbols/error_type_symbol.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 2395 bytes
from pynestml.symbols.type_symbol import TypeSymbol

class ErrorTypeSymbol(TypeSymbol):
    __doc__ = "\n    Originally intended to only be a 'Null type' for the TypeSymbol hierarchy,\n    it is now also a device to communicate errors and warnings back to a place where they can be properly logged\n    (we cant do that here because we don't know t he source-position).\n    Thought about using Exceptions but that would lead to loads of code duplication in the\n    visitors responsible for expression typing.\n    In the end a little bit of ugliness here saves us a lot throughout the project -ptraeder\n\n    p.s. could possibly resolve this by associating type-symbol objects with expressions they belong to.\n    The field for that is already present from Symbol and we already instantiate types for every expression\n    anyways\n    "

    def is_numeric(self):
        return False

    def print_nestml_type(self):
        return 'error'

    def is_primitive(self):
        return False

    def __init__(self):
        super(ErrorTypeSymbol, self).__init__(name='error')

    def __mul__(self, other):
        return self

    def __mod__(self, other):
        return self

    def __truediv__(self, other):
        return self

    def __div__(self, other):
        return self

    def __neg__(self):
        return self

    def __pos__(self):
        return self

    def __invert__(self):
        return self

    def __pow__(self, power, modulo=None):
        return self

    def negate(self):
        return self

    def __add__(self, other):
        return self

    def __sub__(self, other):
        return self

    def is_castable_to(self, _other_type):
        return False