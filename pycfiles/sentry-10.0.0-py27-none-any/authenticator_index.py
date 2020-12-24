# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/authenticator_index.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from sentry.api.base import Endpoint
from sentry.models import Authenticator

class AuthenticatorIndexEndpoint(Endpoint):
    permission_classes = (
     IsAuthenticated,)

    def get(self, request):
        """Returns u2f interface for a user, otherwise an empty array
        """
        try:
            interface = Authenticator.objects.get_interface(request.user, 'u2f')
            if not interface.is_enrolled:
                raise LookupError()
        except LookupError:
            return Response([])

        challenge = interface.activate(request._request).challenge
        return Response([{'id': 'u2f', 'challenge': challenge}])