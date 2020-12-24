# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_auth_provider_send_reminders.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from sentry import features
from sentry.api.bases.organization import OrganizationEndpoint, OrganizationAdminPermission
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.models import AuthProvider
from sentry.tasks.auth import email_missing_links
ERR_NO_SSO = _('The SSO feature is not enabled for this organization.')

class OrganizationAuthProviderSendRemindersEndpoint(OrganizationEndpoint):
    permission_classes = (
     OrganizationAdminPermission,)

    def post(self, request, organization):
        if not features.has('organizations:sso-basic', organization, actor=request.user):
            return Response(ERR_NO_SSO, status=403)
        try:
            auth_provider = AuthProvider.objects.get(organization=organization)
        except AuthProvider.DoesNotExist:
            raise ResourceDoesNotExist

        email_missing_links.delay(organization.id, request.user.id, auth_provider.key)
        return Response(status=200)