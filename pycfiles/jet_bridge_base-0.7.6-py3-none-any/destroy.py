# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/views/mixins/destroy.py
# Compiled at: 2019-10-06 13:11:23
from jet_bridge_base import status
from jet_bridge_base.responses.json import JSONResponse

class DestroyAPIViewMixin(object):

    def delete(self, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JSONResponse(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        self.session.delete(instance)
        self.session.commit()