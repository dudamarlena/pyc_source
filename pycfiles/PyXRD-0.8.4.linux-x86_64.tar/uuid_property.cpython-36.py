# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/models/properties/uuid_property.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1698 bytes
from .labeled_property import LabeledProperty

class UUIDProperty(LabeledProperty):
    __doc__ = "\n     A descriptor that handles removing and adding objects to a pool of unique\n     objects. Expects the class type of the instance having this property to\n     implement a 'remove_object' and 'add_object' method.\n    "

    def __set__(self, instance, value):
        type(instance).object_pool.remove_object(instance)
        retval = super(UUIDProperty, self).__set__(instance, value)
        type(instance).object_pool.add_object(instance)
        return retval