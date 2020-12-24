# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/resources/mixins/queries.py
# Compiled at: 2019-06-12 01:17:17
"""Mixins for helping with lookups from HTTP GET query strings."""
from __future__ import unicode_literals
from django.db.models import Q

class APIQueryUtilsMixin(object):
    """Adds useful functions to a WebAPIResource for database lookups."""

    def build_queries_for_int_field(self, request, field_name, query_param_name=None):
        """Build queries based on request parameters for an int field.

        :py:meth:`get_queryset` implementations can use this to allow callers
        to filter results through range matches. Callers can search for exact
        matches, or can make use of the following operations:

        * ``<`` (:samp:`?{name}-lt={value}`)
        * ``<=`` (:samp:`?{name}-lte={value}`)
        * ``>`` (:samp:`?{name}-gt={value}`)
        * ``>=`` (:samp:`?{name}-gte={value}`)

        Args:
            request (django.http.HttpRequest):
                The HTTP request from the client.

            field_name (unicode):
                The field name in the database to query against.

            query_param_name (unicode):
                The query argument passed to the URL. Defaults to the
                ``field_name``.

        Returns:
            django.db.models.Q:
            A query expression that can be used in database queries.
        """
        if not query_param_name:
            query_param_name = field_name.replace(b'_', b'-')
        q = Q()
        if query_param_name in request.GET:
            q = q & Q(**{field_name: request.GET[query_param_name]})
        for op in ('gt', 'gte', 'lt', 'lte'):
            param = b'%s-%s' % (query_param_name, op)
            if param in request.GET:
                query_field = b'%s__%s' % (field_name, op)
                try:
                    q = q & Q(**{query_field: int(request.GET[param])})
                except ValueError:
                    pass

        return q