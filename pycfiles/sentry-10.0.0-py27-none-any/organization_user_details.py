# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_user_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases.organization import OrganizationEndpoint
from sentry.api.serializers import serialize
from sentry.models import User
from sentry.api.endpoints.organization_member_index import MemberPermission

class OrganizationUserDetailsEndpoint(OrganizationEndpoint):
    permission_classes = (
     MemberPermission,)

    def get(self, request, organization, user_id):
        try:
            user = User.objects.get(id=user_id, sentry_orgmember_set__organization_id=organization.id)
        except User.DoesNotExist:
            return Response(status=404)

        return Response(serialize(user, request.user))