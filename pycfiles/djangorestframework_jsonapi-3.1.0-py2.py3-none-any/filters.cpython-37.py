# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sao/src/github/django-json-api/django-rest-framework-json-api/rest_framework_json_api/filters.py
# Compiled at: 2019-10-02 06:38:51
# Size of source mod 2**32: 4389 bytes
import re
from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend, OrderingFilter
from rest_framework_json_api.utils import format_value

class OrderingFilter(OrderingFilter):
    __doc__ = '\n    A backend filter that implements http://jsonapi.org/format/#fetching-sorting and\n    raises a 400 error if any sort field is invalid.\n\n    If you prefer *not* to report 400 errors for invalid sort fields, just use\n    :py:class:`rest_framework.filters.OrderingFilter` with\n    :py:attr:`~rest_framework.filters.OrderingFilter.ordering_param` = "sort"\n\n    Also applies DJA format_value() to convert (e.g. camelcase) to underscore.\n    (See JSON_API_FORMAT_FIELD_NAMES in docs/usage.md)\n    '
    ordering_param = 'sort'

    def remove_invalid_fields(self, queryset, fields, view, request):
        valid_fields = [item[0] for item in self.get_valid_fields(queryset, view, {'request': request})]
        bad_terms = [term for term in fields if format_value(term.replace('.', '__').lstrip('-'), 'underscore') not in valid_fields]
        if bad_terms:
            raise ValidationError('invalid sort parameter{}: {}'.format('s' if len(bad_terms) > 1 else '', ','.join(bad_terms)))
        underscore_fields = []
        for item in fields:
            item_rewritten = item.replace('.', '__')
            if item_rewritten.startswith('-'):
                underscore_fields.append('-' + format_value(item_rewritten.lstrip('-'), 'underscore'))
            else:
                underscore_fields.append(format_value(item_rewritten, 'underscore'))

        return super(OrderingFilter, self).remove_invalid_fields(queryset, underscore_fields, view, request)


class QueryParameterValidationFilter(BaseFilterBackend):
    __doc__ = '\n    A backend filter that performs strict validation of query parameters for\n    JSON:API spec conformance and raises a 400 error if non-conforming usage is\n    found.\n\n    If you want to add some additional non-standard query parameters,\n    override :py:attr:`query_regex` adding the new parameters. Make sure to comply with\n    the rules at http://jsonapi.org/format/#query-parameters.\n    '
    query_regex = re.compile('^(sort|include)$|^(filter|fields|page)(\\[[\\w\\.\\-]+\\])?$')

    def validate_query_params(self, request):
        """
        Validate that query params are in the list of valid query keywords in
        :py:attr:`query_regex`

        :raises ValidationError: if not.
        """
        for qp in request.query_params.keys():
            if not self.query_regex.match(qp):
                raise ValidationError('invalid query parameter: {}'.format(qp))
            if len(request.query_params.getlist(qp)) > 1:
                raise ValidationError('repeated query parameter not allowed: {}'.format(qp))

    def filter_queryset(self, request, queryset, view):
        """
        Overrides :py:meth:`BaseFilterBackend.filter_queryset` by first validating the
        query params with :py:meth:`validate_query_params`
        """
        self.validate_query_params(request)
        return queryset