# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/user_social_identities_index.py
# Compiled at: 2019-08-16 12:27:40
from __future__ import absolute_import
from rest_framework.response import Response
from social_auth.models import UserSocialAuth
from sentry.api.bases.user import UserEndpoint
from sentry.api.serializers import serialize

class UserSocialIdentitiesIndexEndpoint(UserEndpoint):

    def get(self, request, user):
        """
        List Account's Identities
        `````````````````````````

        List an account's associated identities (e.g. github when trying to add a repo)

        :auth: required
        """
        identity_list = list(UserSocialAuth.objects.filter(user=user))
        return Response(serialize(identity_list))