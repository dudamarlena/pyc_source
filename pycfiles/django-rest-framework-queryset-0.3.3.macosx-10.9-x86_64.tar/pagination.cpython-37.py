# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jlin/virtualenvs/django-rest-framework-queryset/lib/python3.7/site-packages/rest_framework_queryset/pagination.py
# Compiled at: 2019-05-01 00:34:06
# Size of source mod 2**32: 1297 bytes
from __future__ import unicode_literals
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class HybridPagination(PageNumberPagination):
    __doc__ = "\n    Basically allows both pagination method to work within a single pagination class.\n    By default it uses the PageNumberPagination\n    When 'offset' is used in request.GET, it will switch to use LimitOffsetPagination\n    "
    page_size = 10
    default_limit = 1

    def __init__(self, *args, **kwargs):
        self.proxy = None
        return (super(HybridPagination, self).__init__)(*args, **kwargs)

    def paginate_queryset(self, queryset, request, view=None):
        if 'offset' in request.GET or 'limit' in request.GET:
            self.proxy = LimitOffsetPagination()
            return self.proxy.paginate_queryset(queryset, request, view)
        return super(HybridPagination, self).paginate_queryset(queryset, request, view)

    def __getattribute__(self, item):
        if item in ('paginate_queryset', ):
            return object.__getattribute__(self, item)
        try:
            proxy = object.__getattribute__(self, 'proxy')
            return object.__getattribute__(proxy, item)
        except AttributeError:
            return object.__getattribute__(self, item)