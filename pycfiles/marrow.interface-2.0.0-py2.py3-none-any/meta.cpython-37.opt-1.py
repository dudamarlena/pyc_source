# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/interface/meta.py
# Compiled at: 2019-01-21 15:04:55
# Size of source mod 2**32: 1883 bytes
from inspect import isclass
from marrow.schema.meta import ElementMeta
from .schema import Attribute
__all__ = [
 'InterfaceMeta', 'Interface']
ALLOWED_PROPERTIES = ('__doc__', '__module__', '__assume__', '__assume_interface__',
                      '__qualname__', '__sequence__', '__locals__')

class InterfaceMeta(ElementMeta):
    __doc__ = 'As per marrow.schema.meta:ElementMeta, but with additional restrictions.\n\t\n\tAdditionally, this metaclass overrides `isinstance` behaviour on participatory objects.\n\t'

    def __new__(meta, name, bases, attrs):
        if bases == (object,):
            return ElementMeta.__new__(meta, name, bases, attrs)
        for key in attrs:
            if key in ALLOWED_PROPERTIES:
                continue
            if not isinstance(attrs[key], Attribute):
                raise TypeError('Interfaces must only contain Attribute instances, not a {0} named {1}.'.format(type(attrs[key]).__name__, key))

        for base in bases:
            if type(base) is not InterfaceMeta:
                raise TypeError('Do not mix interfaces with other base classes.')

        return ElementMeta.__new__(meta, name, bases, attrs)

    def __instancecheck__(cls, inst, live=True):
        """Does the given instance support this interface?"""
        return cls.implements(inst)

    def implements(interface, instance):
        assumptions = getattr(interface, '__assume__', getattr(interface, '__assume_interface__', []))
        if isclass(instance):
            if issubclass(instance, tuple(assumptions)):
                return True
        if isinstance(instance, tuple(assumptions)):
            return True
        for i, j in interface.__attributes__.items():
            if not j(instance):
                return False

        return True


Interface = InterfaceMeta('Interface', (object,), dict())