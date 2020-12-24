# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/working/eventum/eventum/models/BaseEventumDocument.py
# Compiled at: 2016-04-19 10:47:47
import types

class BaseEventumDocument(object):
    _registered_attributes = []

    @classmethod
    def deregister_attribute(cls, name):
        if name not in cls._registered_attributes:
            raise ValueError('Cannot delete attribute.')
        cls._registered_attributes.remove(name)
        delattr(cls, name)

    @classmethod
    def register_method(cls, method):
        if hasattr(cls, method.__name__):
            raise ValueError('Method exists.')
        cls._registered_attributes.append(method.__name__)
        return setattr(cls, method.__name__, types.MethodType(method, None, cls))