# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/views/mixins/list.py
# Compiled at: 2019-10-06 13:11:29
from jet_bridge_base.responses.json import JSONResponse

class ListAPIViewMixin(object):

    def list(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer.representation_data)
        else:
            serializer = self.get_serializer(instance=queryset, many=True)
            return JSONResponse(serializer.representation_data)