# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ricard/develop/my_django_tweaks/my_django_tweaks/pagination.py
# Compiled at: 2019-05-17 08:43:05
# Size of source mod 2**32: 4999 bytes
from collections import OrderedDict
import django.utils.translation as _
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.pagination import LimitOffsetPagination, NotFound, PageNumberPagination, remove_query_param, replace_query_param
from rest_framework.response import Response

class IncorrectLimitOffsetError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Incorrect offset or limit.')


class NoCountsLimitOffsetPagination(LimitOffsetPagination):
    __doc__ = '\n    A limit/offset based pagination, without performing counts. For example:\n\n    http://api.example.org/accounts/?limit=100 - will return first 100 items\n    http://api.example.org/accounts/?offset=400&limit=100 - will returns 100 items starting from 401th\n    http://api.example.org/accounts/?offset=-50&limit=100 - will return first 50 items\n\n    HTML is not handled (no get_html_context).\n\n    Pros:\n        - no counts\n        - easier to use than cursor pagination (especially if you need sorting)\n        - works with angular ui-scroll (which requires negative offsets)\n\n    Cons:\n        - skip is a relatively slow operation, so this paginator is not as fast as cursor paginator when you use\n          large offsets\n    '

    def get_html_context(self):
        raise NotImplementedError

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit is None:
            raise IncorrectLimitOffsetError
        self.offset = self.get_offset(request)
        self.effective_limit = self.limit
        if self.offset < 0:
            self.effective_limit += self.offset
            self.offset = 0
        if self.effective_limit <= 0:
            raise IncorrectLimitOffsetError
        self.request = request
        self.results = list(queryset[self.offset:self.offset + self.effective_limit])
        return self.results

    def get_paginated_response(self, data):
        return Response(OrderedDict([
         (
          'next', self.get_next_link()),
         (
          'previous', self.get_previous_link()),
         (
          'results', data)]))

    def get_offset(self, request):
        try:
            return int(request.query_params[self.offset_query_param])
        except (KeyError, ValueError):
            return 0

    def get_next_link(self):
        if len(self.results) < self.effective_limit:
            return
        url = self.request.build_absolute_uri()
        url = replace_query_param(url, self.limit_query_param, self.limit)
        offset = self.offset + self.effective_limit
        return replace_query_param(url, self.offset_query_param, offset)


class NoCountsPageNumberPagination(PageNumberPagination):
    __doc__ = '\n    A standard page number pagination, without performing counts.\n\n    HTML is not handled (no get_html_context).\n\n    Pros:\n        - no counts\n        - easier to use than cursor pagination (especially if you need sorting)\n\n    Cons:\n        - skip is a relatively slow operation, so this paginator is not as fast as cursor paginator when you use\n          large page numbers\n    '

    def get_page_number(self, request):
        try:
            return int(request.query_params[self.page_query_param])
        except (KeyError, ValueError):
            return 1

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        self.page_size = self.get_page_size(request)
        if not self.page_size:
            return
        self.page_number = self.get_page_number(request)
        if self.page_number < 1:
            raise NotFound(self.invalid_page_message)
        self.request = request
        self.results = list(queryset[(self.page_number - 1) * self.page_size:self.page_number * self.page_size])
        return self.results

    def get_paginated_response(self, data):
        return Response(OrderedDict([
         (
          'next', self.get_next_link()),
         (
          'previous', self.get_previous_link()),
         (
          'results', data)]))

    def get_next_link(self):
        if len(self.results) < self.page_size:
            return
        url = self.request.build_absolute_uri()
        next_page_number = self.page_number + 1
        return replace_query_param(url, self.page_query_param, next_page_number)

    def get_previous_link(self):
        if self.page_number == 1:
            return
        url = self.request.build_absolute_uri()
        previous_page_number = self.page_number - 1
        if previous_page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, previous_page_number)