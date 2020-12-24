# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/FinanceFields/CurrencyField.py
# Compiled at: 2010-03-10 14:21:02
from Products.Archetypes.public import *

class CurrencyField(ObjectField):
    """A field that stores currency"""
    __module__ = __name__
    _properties = Field._properties.copy()
    _properties.update({'type': 'currency', 'default': None})

    def set(self, instance, value, **kwargs):
        """Convert passed-in value to a currency. If failure, set value to
        None."""
        if value == '':
            value = None
        elif value is not None:
            __traceback_info__ = (self.getName(), instance, value, kwargs)
            value = float(value)
        ObjectField.set(self, instance, value, **kwargs)
        return