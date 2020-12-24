# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/value.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 3006 bytes
"""PyAMS_form.value module

Simple value adapters.
"""
from zope.component import adapter
from zope.interface import implementer
from pyams_form.interfaces import IValue
from pyams_form.util import get_specification
__docformat__ = 'restructuredtext'

@implementer(IValue)
class StaticValue:
    __doc__ = 'Static value adapter.'

    def __init__(self, value):
        self.value = value

    def get(self):
        """Get static value"""
        return self.value

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.value)


@implementer(IValue)
class ComputedValue:
    __doc__ = 'Computed value adapter.'

    def __init__(self, func):
        self.func = func

    def get(self):
        """Get computed value"""
        return self.func(self)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.get())


class ValueFactory:
    __doc__ = 'Computed value factory.'

    def __init__(self, value, value_class, discriminators):
        self.value = value
        self.value_class = value_class
        self.discriminators = discriminators

    def __call__(self, *args):
        value_class = self.value_class(self.value)
        for name, value in zip(self.discriminators, args):
            setattr(value_class, name, value)

        return value_class


class ValueCreator:
    __doc__ = 'Base class for value creator'
    value_class = StaticValue

    def __init__(self, discriminators):
        self.discriminators = discriminators

    def __call__(self, value, **kws):
        if set(kws).difference(set(self.discriminators)):
            raise ValueError('One or more keyword arguments did not match the discriminators.')
        factory = ValueFactory(value, self.value_class, self.discriminators)
        signature = []
        for disc in self.discriminators:
            spec = get_specification(kws.get(disc))
            signature.append(spec)

        adapter(*signature)(factory)
        implementer(IValue)(factory)
        return factory


class StaticValueCreator(ValueCreator):
    __doc__ = 'Creates static value.'
    value_class = StaticValue


class ComputedValueCreator(ValueCreator):
    __doc__ = 'Creates computed value.'
    value_class = ComputedValue