# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/utils/serializers.py
# Compiled at: 2019-10-27 19:02:52
# Size of source mod 2**32: 1882 bytes
from .actions import Actions

class SerializerMapping(object):
    DEFAULT_ACTION = Actions.CREATE

    def __init__(self, mapping):
        assert isinstance(mapping, dict)
        assert self.DEFAULT_ACTION in mapping
        self.serializer_mapping = mapping

    def get_serializer_class(self, action):
        try:
            return self.serializer_mapping[action]
        except KeyError:
            return self.serializer_mapping[self.DEFAULT_ACTION]

    @classmethod
    def from_module(cls, module):
        serializer_mapping = {}
        if hasattr(module, 'ListSerializer'):
            serializer_mapping[Actions.LIST] = module.ListSerializer
        if hasattr(module, 'CreateSerializer'):
            serializer_mapping[Actions.CREATE] = module.CreateSerializer
        if hasattr(module, 'DetailSerializer'):
            serializer_mapping[Actions.RETRIEVE] = module.DetailSerializer
        if hasattr(module, 'UpdateSerializer'):
            serializer_mapping[Actions.UPDATE] = module.UpdateSerializer
            serializer_mapping[Actions.PARTIAL_UPDATE] = module.UpdateSerializer
        if hasattr(module, 'MetadataSerializer'):
            serializer_mapping[Actions.METADATA] = module.MetadataSerializer
        return cls(serializer_mapping)

    def extend(self, additional_actions=None, **kwargs):
        if additional_actions is None:
            additional_actions = {}
        extended_mapping = self.serializer_mapping.copy()
        extended_mapping.update(additional_actions)
        for key in kwargs:
            extended_mapping[key] = kwargs[key]

        return SerializerMapping(extended_mapping)


class SerializerMappingMixin(object):

    @property
    def serializer_mapping(self):
        raise NotImplementedError

    def get_serializer_class(self):
        return self.serializer_mapping.get_serializer_class(self.action)