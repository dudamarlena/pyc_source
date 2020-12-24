# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/relay_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.models import Relay
from sentry.api.base import Endpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.api.permissions import SuperuserPermission

class RelayDetailsEndpoint(Endpoint):
    permission_classes = (
     SuperuserPermission,)

    def delete(self, request, relay_id):
        """
        Delete one Relay
        ````````````````
        :auth: required
        """
        try:
            relay = Relay.objects.get(id=relay_id)
        except Relay.DoesNotExist:
            raise ResourceDoesNotExist

        relay.delete()
        return Response(status=204)