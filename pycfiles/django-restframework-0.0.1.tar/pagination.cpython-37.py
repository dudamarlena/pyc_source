# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cox/Documents/GitHub/django_rest_framework/django_restframework/paginations/pagination.py
# Compiled at: 2019-04-22 15:07:06
# Size of source mod 2**32: 1065 bytes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
import math

class MyPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 500
    page_query_param = 'page'

    def get_total_pages(self):
        """总页数"""
        return math.ceil(self.page.paginator.count / self.page_size)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
         (
          'count', self.page.paginator.count),
         (
          'size', self.page_size),
         (
          'totalpages', self.get_total_pages()),
         ('success', True),
         ('msg', 'ok'),
         (
          'next', self.get_next_link()),
         (
          'previous', self.get_previous_link()),
         (
          'results', data)]))