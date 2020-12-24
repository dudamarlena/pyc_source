# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/glyph/resource/persistent.py
# Compiled at: 2012-03-18 14:24:57
from uuid import uuid4
from .base import ClassMapper, BaseResource
from .handler import redirect

class PersistentMapper(ClassMapper):

    def __init__(self, prefix, res):
        ClassMapper.__init__(self, prefix, res)
        self.instances = {}
        self.identifiers = {}

    @redirect()
    def POST(self, **args):
        instance = self.res(**args)
        uuid = str(uuid4())
        self.instances[uuid] = instance
        self.identifiers[instance] = uuid
        return instance

    def get_instance(self, uuid):
        return self.instances[uuid]

    def get_repr(self, instance):
        if instance not in self.identifiers:
            uuid = str(uuid4())
            self.instances[uuid] = instance
            self.identifiers[instance] = uuid
        else:
            uuid = self.identifiers[instance]
        return uuid


class PersistentResource(BaseResource):
    __glyph__ = PersistentMapper