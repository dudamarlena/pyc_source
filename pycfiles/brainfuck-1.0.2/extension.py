# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/brainfreeze/extension.py
# Compiled at: 2008-11-10 02:21:45
__doc__ = 'OneToOne MapperExtension'
from sqlalchemy import util
from sqlalchemy.orm import MapperExtension, class_mapper, EXT_CONTINUE
from sqlalchemy.exceptions import ArgumentError
from properties import one_to_one
__all__ = [
 'OneToOneMapperExtension']

class OneToOneMapperExtension(MapperExtension):
    """MapperExtension to proxy properties on one-to-one relations.

    This extension proxies access to all properties of the specified
    one-to-one relations without an intermediate layer. 
    
    The intended use case is to allow a type composed of multiple tables to
    be easily mapped and queried as if it were one table.

    """

    def __init__(self, *related_classes, **kwargs):
        if len(util.to_list(related_classes)) != len(util.to_set(related_classes)):
            raise ArgumentError('Name collision, classes may only be specified once: %r' % related_classes)
        self.related_classes = util.to_list(related_classes)
        self.property_prefix = kwargs.get('property_prefix', '_')

    def instrument_class(self, mapper, class_):
        for value_class in self.related_classes:
            value_mapper = class_mapper(value_class, compile=False)
            key = self.property_prefix + value_mapper.local_table.key
            if key in mapper._init_properties:
                raise ArgumentError("OneToOne relation '%s' conflicts with existing property" % key)
            mapper._init_properties[key] = one_to_one(value_class)

        return EXT_CONTINUE