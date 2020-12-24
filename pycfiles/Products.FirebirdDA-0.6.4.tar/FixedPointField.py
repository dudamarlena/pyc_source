# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/FinanceFields/FixedPointField.py
# Compiled at: 2010-03-10 14:21:02
__doc__ = 'FixedPointField is an archetypes field that can be used to represent\nfixed point values.\n\n$Id: CustomFields.py 33 2005-07-04 21:12:23Z roche $\n'
from types import TupleType
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import ObjectField, DecimalWidget
from Products.Archetypes.Registry import registerField
from MoneyWidget import MoneyWidget
from Currency import CURRENCIES
from Money import Money, parseString
from fixedpoint import FixedPoint

class FixedPointField(ObjectField):
    """A field for storing fixed point values"""
    __module__ = __name__
    __implements__ = ObjectField.__implements__
    _properties = ObjectField._properties.copy()
    _properties.update({'type': 'FixedPoint', 'widget': DecimalWidget, 'validators': 'isDecimal'})
    security = ClassSecurityInfo()
    security.declarePrivate('set')

    def set(self, instance, value, **kwargs):
        """
        Check if value is an actual FixedPoint value. If not, attempt to
        convert it to one; Raise an error if value is a float. Assign
        all properties passed as kwargs to object.

        field.set( FixedPoint(10))
        field.set( FixedPointInstance)

        """
        assert type(value) != type(0.0)
        if value is not None and not isinstance(value, FixedPoint):
            value = FixedPoint(value)
        ObjectField.set(self, instance, value, **kwargs)
        return


registerField(FixedPointField, title='FixedPoint', description='Used for storing FixedPoint')