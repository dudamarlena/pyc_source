# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/alchemist/property.py
# Compiled at: 2008-09-11 20:29:53
"""
Binding Zope3 Schema Properties to Alchemist Mapped Classes

$Id: property.py 299 2008-05-23 20:31:48Z kapilt $
"""
from sqlalchemy.orm import attributes
from interfaces import IIModelInterface
from zope import schema, interface

class ValidatedProperty(object):
    """
    Computed attributes based on schema fields that collaborate with sqlalchemy
    properties, and provide validation, error messages, and default values.
    """

    def __init__(self, field, prop, name=None):
        self.__field = field
        self.__prop = prop
        self.__name = name or field.__name__

    def __get__(self, inst, klass):
        if inst is None:
            return self
        return self.__prop.__get__(inst, klass)

    def __getattr__(self, name):
        return getattr(self.__prop, name)

    def __set__(self, inst, value):
        field = self.__field.bind(inst)
        field.validate(value)
        if field.readonly and inst.__dict__.has_key(self.__name):
            raise ValueError(self.__name, 'field is readonly')
        self.__prop.__set__(inst, value)

    def __delete__(self, obj):
        if self.__field.readonly and obj.__dict__.has_key(self.__name):
            raise ValueError(self.__name, 'field is readonly')
        self.__prop.__delete__(obj)


def bindClass(klass, mapper=None):
    """
    attach validation to a sqlalchemy mapped class, based on its implemented schemas, via property
    validators, taking care to wrap sqlalchemy properties.
    """
    if mapper is None:
        mapper = getattr(klass, 'mapper')
    mapper.compile()
    for iface in interface.implementedBy(klass):
        if not IIModelInterface.providedBy(iface):
            continue
        for field_name in schema.getFieldNames(iface):
            v = klass.__dict__.get(field_name)
            if not isinstance(v, attributes.InstrumentedAttribute):
                continue
            field = iface[field_name]
            vproperty = ValidatedProperty(field, v, field_name)
            setattr(klass, field_name, vproperty)

    return