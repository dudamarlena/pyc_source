# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/views/mixins/list.py
# Compiled at: 2019-11-10 07:24:54
# Size of source mod 2**32: 747 bytes
from jet_bridge_base.responses.json import JSONResponse

class ListAPIViewMixin(object):

    def list(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginate = not self.request.get_argument('_no_pagination', False)
        page = self.paginate_queryset(queryset) if paginate else None
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer.representation_data)
        else:
            if queryset._limit is None:
                queryset = queryset.limit(10000)
            serializer = self.get_serializer(instance=queryset, many=True)
            data = serializer.representation_data
            return JSONResponse(data)