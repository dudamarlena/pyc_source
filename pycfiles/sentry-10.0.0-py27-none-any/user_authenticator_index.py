# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/user_authenticator_index.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases.user import UserEndpoint
from sentry.api.serializers import serialize
from sentry.models import Authenticator

class UserAuthenticatorIndexEndpoint(UserEndpoint):

    def get(self, request, user):
        """Returns all interface for a user (un-enrolled ones), otherwise an empty array
        """
        interfaces = Authenticator.objects.all_interfaces_for_user(user, return_missing=True)
        return Response(serialize(list(interfaces)))