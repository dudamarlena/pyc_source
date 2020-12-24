# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/builtin_symbol_sources.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
import six
from django.conf import settings
from sentry.api.base import Endpoint
from sentry.api.serializers import serialize

def normalize_symbol_source(key, source):
    return {'sentry_key': key, 'id': source['id'], 'name': source['name']}


class BuiltinSymbolSourcesEndpoint(Endpoint):
    permission_classes = ()

    def get(self, request):
        sources = [ normalize_symbol_source(key, source) for key, source in six.iteritems(settings.SENTRY_BUILTIN_SOURCES)
                  ]
        sources.sort(key=lambda s: s['name'])
        return Response(serialize(sources))