# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/serializers/model_group.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 563 bytes
from jet_bridge_base.fields import CharField
from jet_bridge_base.serializers.serializer import Serializer

class ModelGroupSerializer(Serializer):
    group = CharField()
    y_func = CharField()

    def __init__(self, *args, **kwargs):
        if 'group_serializer' in kwargs:
            self.fields['group'] = kwargs.pop('group_serializer')
        if 'y_func_serializer' in kwargs:
            self.fields['y_func'] = kwargs.pop('y_func_serializer')
        super(ModelGroupSerializer, self).__init__(*args, **kwargs)