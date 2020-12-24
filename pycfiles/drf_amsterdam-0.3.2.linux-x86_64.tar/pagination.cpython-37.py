# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3393)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stephan/.virtualenvs/drf_amsterdam/lib/python3.7/site-packages/datapunt_api/pagination.py
from collections import OrderedDict
from rest_framework import pagination, response
from rest_framework.utils.urls import replace_query_param

class HALPagination(pagination.PageNumberPagination):
    __doc__ = 'Implement HAL-JSON style pagination.\n\n    used on most rest Datapunt APIs.\n    '
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        self_link = self.request.build_absolute_uri()
        if self_link.endswith('.api'):
            self_link = self_link[:-4]
        else:
            if self.page.has_next():
                next_link = replace_query_param(self_link, self.page_query_param, self.page.next_page_number())
            else:
                next_link = None
            if self.page.has_previous():
                prev_link = replace_query_param(self_link, self.page_query_param, self.page.previous_page_number())
            else:
                prev_link = None
        return response.Response(OrderedDict([
         (
          '_links',
          OrderedDict([
           (
            'self', dict(href=self_link)),
           (
            'next', dict(href=next_link)),
           (
            'previous', dict(href=prev_link))])),
         (
          'count', self.page.paginator.count),
         (
          'results', data)]))


class HALCursorPagination(pagination.CursorPagination):
    __doc__ = 'Implement HAL-JSON Cursor style pagination.\n\n    standard for large datasets Datapunt REST APIs.\n    '
    page_size_query_param = 'page_size'
    count_table = False
    count = 0

    def paginate_queryset(self, queryset, request, view=None):
        if self.count_table:
            self.count = queryset.count()
        return super(HALCursorPagination, self).paginate_queryset(queryset, request, view=view)

    def get_paginated_response(self, data):
        self_link = self.base_url
        if self_link.endswith('.api'):
            self_link = self_link[:-4]
        next_link = self.get_next_link()
        previous_link = self.get_previous_link()
        _response = OrderedDict([
         (
          '_links',
          OrderedDict([
           (
            'next', dict(href=next_link)),
           (
            'previous', dict(href=previous_link))])),
         (
          'count', self.count),
         (
          'results', data)])
        if not self.count_table:
            _response.pop('count')
        return response.Response(_response)