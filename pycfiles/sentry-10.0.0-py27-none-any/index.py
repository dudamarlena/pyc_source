# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/index.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.base import Endpoint
from sentry.api.serializers import serialize
from sentry.utils.functional import extract_lazy_object

class IndexEndpoint(Endpoint):
    permission_classes = ()

    def get(self, request):
        if request.user.is_authenticated():
            user = serialize(extract_lazy_object(request.user), request.user)
        else:
            user = None
        if request.auth:
            auth = {'scopes': request.auth.get_scopes()}
        else:
            auth = None
        context = {'version': '0', 'auth': auth, 'user': user}
        return Response(context, status=200)