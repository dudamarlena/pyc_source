# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tony/Projects/django-rest-framework-word-search-filter/rest_framework_word_filter/filter.py
# Compiled at: 2015-05-05 09:10:57
# Size of source mod 2**32: 2001 bytes
import operator
from django.db import models
from django.utils.six.moves import reduce
from rest_framework.filters import BaseFilterBackend
from rest_framework.settings import api_settings

class FullWordSearchFilter(BaseFilterBackend):
    search_param = api_settings.SEARCH_PARAM

    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        params = request.query_params.get(self.search_param, '')
        return params.replace(',', ' ').split()

    @staticmethod
    def construct_search(field_name):
        return ['{}__icontains'.format(field_name),
         '{}__istartswith'.format(field_name),
         '{}__iendswith'.format(field_name),
         '{}__exact'.format(field_name)]

    @staticmethod
    def construct_term(term):
        return [' {} '.format(term),
         '{} '.format(term),
         ' {}'.format(term),
         term]

    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'word_fields', None)
        if not search_fields:
            return queryset
        orm_lookups = [self.construct_search(str(search_field)) for search_field in search_fields]
        search_term = request.query_params.get(self.search_param, '').split()
        if not search_term:
            return queryset
        lookup_list = list()
        for orm_lookup in orm_lookups:
            and_query = list()
            for term in search_term:
                and_query.append(reduce(operator.or_, [models.Q(**{lookup: prep_term}) for lookup, prep_term in zip(orm_lookup, self.construct_term(term))]))

            lookup_list.append(reduce(operator.and_, and_query))

        queryset = queryset.filter(reduce(operator.or_, lookup_list))
        return queryset