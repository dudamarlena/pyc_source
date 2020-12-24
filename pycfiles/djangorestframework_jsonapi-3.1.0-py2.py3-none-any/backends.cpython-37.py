# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sao/src/github/django-json-api/django-rest-framework-json-api/rest_framework_json_api/django_filters/backends.py
# Compiled at: 2019-10-02 06:38:51
# Size of source mod 2**32: 5275 bytes
import re
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from rest_framework_json_api.utils import format_value

class DjangoFilterBackend(DjangoFilterBackend):
    __doc__ = '\n    A Django-style ORM filter implementation, using `django-filter`.\n\n    This is not part of the jsonapi standard per-se, other than the requirement\n    to use the `filter` keyword: This is an optional implementation of style of\n    filtering in which each filter is an ORM expression as implemented by\n    DjangoFilterBackend and seems to be in alignment with an interpretation of\n    http://jsonapi.org/recommendations/#filtering, including relationship\n    chaining. It also returns a 400 error for invalid filters.\n\n    Filters can be:\n\n    - A resource field\n      equality test:\n\n      ``?filter[qty]=123``\n\n    - Apply other\n      https://docs.djangoproject.com/en/stable/ref/models/querysets/#field-lookups\n      operators:\n\n      ``?filter[name.icontains]=bar`` or ``?filter[name.isnull]=true...``\n\n    - Membership in\n      a list of values:\n\n      ``?filter[name.in]=abc,123,zzz`` (name in [\'abc\',\'123\',\'zzz\'])\n\n    - Filters can be combined\n      for intersection (AND):\n\n      ``?filter[qty]=123&filter[name.in]=abc,123,zzz&filter[...]``\n\n    - A related resource path\n      can be used:\n\n      ``?filter[inventory.item.partNum]=123456`` (where `inventory.item` is the relationship path)\n\n    If you are also using rest_framework.filters.SearchFilter you\'ll want to customize\n    the name of the query parameter for searching to make sure it doesn\'t conflict\n    with a field name defined in the filterset.\n    The recommended value is: `search_param="filter[search]"` but just make sure it\'s\n    `filter[<something>]` to comply with the jsonapi spec requirement to use the filter\n    keyword. The default is "search" unless overriden but it\'s used here just to make sure\n    we don\'t complain about it being an invalid filter.\n    '
    search_param = api_settings.SEARCH_PARAM
    filter_regex = re.compile('^filter(?P<ldelim>\\[?)(?P<assoc>[\\w\\.\\-]*)(?P<rdelim>\\]?$)')

    def _validate_filter(self, keys, filterset_class):
        """
        Check that all the filter[key] are valid.

        :param keys: list of FilterSet keys
        :param filterset_class: :py:class:`django_filters.rest_framework.FilterSet`
        :raises ValidationError: if key not in FilterSet keys or no FilterSet.
        """
        for k in keys:
            if not filterset_class or k not in filterset_class.base_filters:
                raise ValidationError('invalid filter[{}]'.format(k))

    def get_filterset(self, request, queryset, view):
        """
        Sometimes there's no `filterset_class` defined yet the client still
        requests a filter. Make sure they see an error too. This means
        we have to `get_filterset_kwargs()` even if there's no `filterset_class`.
        """
        filterset_class = self.get_filterset_class(view, queryset)
        kwargs = self.get_filterset_kwargs(request, queryset, view)
        self._validate_filter(kwargs.pop('filter_keys'), filterset_class)
        if filterset_class is None:
            return
        return filterset_class(**kwargs)

    def get_filterset_kwargs(self, request, queryset, view):
        """
        Turns filter[<field>]=<value> into <field>=<value> which is what
        DjangoFilterBackend expects

        :raises ValidationError: for bad filter syntax
        """
        filter_keys = []
        data = request.query_params.copy()
        for qp, val in request.query_params.items():
            m = self.filter_regex.match(qp)
            if m:
                if not m.groupdict()['assoc'] or m.groupdict()['ldelim'] != '[' or m.groupdict()['rdelim'] != ']':
                    raise ValidationError('invalid query parameter: {}'.format(qp))
            if m and qp != self.search_param:
                if not val:
                    raise ValidationError('missing {} test value'.format(qp))
                key = m.groupdict()['assoc'].replace('.', '__')
                key = format_value(key, 'underscore')
                data[key] = val
                filter_keys.append(key)
                del data[qp]

        return {'data':data, 
         'queryset':queryset, 
         'request':request, 
         'filter_keys':filter_keys}