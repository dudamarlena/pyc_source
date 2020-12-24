# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/views/mixins/update.py
# Compiled at: 2019-10-13 08:04:40
from jet_bridge_base.responses.json import JSONResponse

class UpdateAPIViewMixin(object):

    def update(self, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=self.request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JSONResponse(serializer.representation_data)

    def put(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def patch(self, *args, **kwargs):
        self.update(partial=True, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(*args, **kwargs)