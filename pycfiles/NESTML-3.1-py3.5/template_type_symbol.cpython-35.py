# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/symbols/template_type_symbol.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1827 bytes
from pynestml.symbols.type_symbol import TypeSymbol

class TemplateTypeSymbol(TypeSymbol):
    __doc__ = 'Function type templates for predefined NESTML functions. This allows e.g. functions like max() and min() to have a return type equal to the type of their arguments, regardless of what type the arguments are (integers, meters, nanosiemens...)\n\n    Template type symbols are uniquely identified with an integer number `i`, i.e. TemplateTypeSymbol(n) == TemplateTypeSymbol(m) iff n == m.'

    def __init__(self, i):
        super(TemplateTypeSymbol, self).__init__(name='_template_' + str(i))
        self._i = i

    def is_numeric(self):
        return False

    def is_primitive(self):
        return True

    def print_nestml_type(self):
        return '_template_' + str(self._i)

    def is_castable_to(self, _other_type):
        if isinstance(_other_type, TemplateTypeSymbol) and _other_type._i == self._i:
            return True
        return False

    def __eq__(self, other):
        if isinstance(other, TemplateTypeSymbol) and other._i == self._i:
            return True
        return False