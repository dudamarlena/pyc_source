# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/relay_publickeys.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.base import Endpoint
from sentry.api.permissions import RelayPermission
from sentry.api.authentication import RelayAuthentication
from sentry.models import Relay

class RelayPublicKeysEndpoint(Endpoint):
    authentication_classes = (
     RelayAuthentication,)
    permission_classes = (RelayPermission,)

    def post(self, request):
        relay_ids = request.relay_request_data.get('relay_ids') or ()
        rv = dict.fromkeys(relay_ids)
        if relay_ids:
            relays = Relay.objects.filter(relay_id__in=relay_ids)
            for relay in relays:
                rv[relay.relay_id] = relay.public_key

        return Response({'public_keys': rv}, status=200)