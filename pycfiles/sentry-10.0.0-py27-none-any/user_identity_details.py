# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/user_identity_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases.user import UserEndpoint
from sentry.models import AuthIdentity

class UserIdentityDetailsEndpoint(UserEndpoint):

    def delete(self, request, user, identity_id):
        AuthIdentity.objects.filter(user=user, id=identity_id).delete()
        return Response(status=204)