# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/paginators/pagination.py
# Compiled at: 2018-12-26 05:23:19


class Pagination(object):
    count = None

    def paginate_queryset(self, queryset, handler):
        raise NotImplementedError

    def get_paginated_response(self, data):
        raise NotImplementedError