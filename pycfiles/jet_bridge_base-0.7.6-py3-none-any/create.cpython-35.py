# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/views/mixins/create.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 820 bytes
from jet_bridge_base import status
from jet_bridge_base.configuration import configuration
from jet_bridge_base.responses.json import JSONResponse

class CreateAPIViewMixin(object):

    def create(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JSONResponse(serializer.representation_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer_instance = serializer.create_instance(serializer.validated_data)
        configuration.on_model_pre_create(self.request.path_kwargs['model'], serializer_instance)
        instance = serializer.save()
        configuration.on_model_post_create(self.request.path_kwargs['model'], instance)