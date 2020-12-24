# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/sentry_app_authorizations.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases import SentryAppAuthorizationsBaseEndpoint
from sentry.coreapi import APIUnauthorized
from sentry.mediators.token_exchange import GrantExchanger, Refresher, GrantTypes
from sentry.api.serializers.models.apitoken import ApiTokenSerializer

class SentryAppAuthorizationsEndpoint(SentryAppAuthorizationsBaseEndpoint):

    def post(self, request, installation):
        try:
            if request.json_body.get('grant_type') == GrantTypes.AUTHORIZATION:
                token = GrantExchanger.run(install=installation, code=request.json_body.get('code'), client_id=request.json_body.get('client_id'), user=request.user)
            elif request.json_body.get('grant_type') == GrantTypes.REFRESH:
                token = Refresher.run(install=installation, refresh_token=request.json_body.get('refresh_token'), client_id=request.json_body.get('client_id'), user=request.user)
            else:
                return Response({'error': 'Invalid grant_type'}, status=403)
        except APIUnauthorized as e:
            return Response({'error': e.msg or 'Unauthorized'}, status=403)

        attrs = {'state': request.json_body.get('state'), 'application': None}
        body = ApiTokenSerializer().serialize(token, attrs, request.user)
        return Response(body, status=201)