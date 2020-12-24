# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/views/mixins/retrieve.py
# Compiled at: 2019-10-07 04:07:11
from jet_bridge_base.responses.json import JSONResponse

class RetrieveAPIViewMixin(object):

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        return JSONResponse(serializer.representation_data)