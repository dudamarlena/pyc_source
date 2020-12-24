# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/views/mixins/destroy.py
# Compiled at: 2019-11-08 11:55:37
# Size of source mod 2**32: 850 bytes
from jet_bridge_base import status
from jet_bridge_base.configuration import configuration
from jet_bridge_base.responses.json import JSONResponse
from jet_bridge_base.utils.exceptions import validation_error_from_database_error

class DestroyAPIViewMixin(object):

    def delete(self, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JSONResponse(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        configuration.on_model_pre_delete(self.request.path_kwargs['model'], instance)
        self.session.delete(instance)
        try:
            self.session.commit()
        except Exception as e:
            raise validation_error_from_database_error(e, self.model)

        configuration.on_model_post_delete(self.request.path_kwargs['model'], instance)