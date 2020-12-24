# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/accept_organization_invite.py
# Compiled at: 2019-08-23 05:13:18
from __future__ import absolute_import
from rest_framework import status
from rest_framework.response import Response
from django.core.urlresolvers import reverse
from sentry.utils import auth
from sentry.api.base import Endpoint
from sentry.models import OrganizationMember, AuthProvider
from sentry.api.invite_helper import ApiInviteHelper

class AcceptOrganizationInvite(Endpoint):
    permission_classes = []

    def respond_invalid(self, request):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'details': 'Invalid invite code'})

    def get_helper(self, request, member_id, token):
        return ApiInviteHelper(instance=self, request=request, member_id=member_id, token=token)

    def get(self, request, member_id, token):
        try:
            helper = self.get_helper(request, member_id, token)
        except OrganizationMember.DoesNotExist:
            return self.respond_invalid(request)

        if not helper.member_pending or not helper.valid_token:
            return self.respond_invalid(request)
        else:
            om = helper.om
            organization = om.organization
            request.session['invite_email'] = om.email
            try:
                auth_provider = AuthProvider.objects.get(organization=organization)
            except AuthProvider.DoesNotExist:
                auth_provider = None

            data = {'orgSlug': organization.slug, 
               'needsAuthentication': not helper.user_authenticated, 
               'needs2fa': helper.needs_2fa, 
               'needsSso': auth_provider is not None, 
               'existingMember': helper.member_already_exists}
            if auth_provider is not None:
                provider = auth_provider.get_provider()
                data['ssoProvider'] = provider.name
            if not helper.user_authenticated:
                url = reverse('sentry-accept-invite', args=[member_id, token])
                auth.initiate_login(self.request, next_url=url)
                request.session['can_register'] = True
            response = Response(data)
            if helper.needs_2fa:
                helper.add_invite_cookie(request, response, member_id, token)
            return response

    def post(self, request, member_id, token):
        try:
            helper = self.get_helper(request, member_id, token)
        except OrganizationMember.DoesNotExist:
            return self.respond_invalid(request)

        if not helper.valid_request:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'details': 'unable to accept organization invite'})
        if helper.member_already_exists:
            response = Response(status=status.HTTP_400_BAD_REQUEST, data={'details': 'member already exists'})
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT)
        helper.accept_invite()
        helper.remove_invite_cookie(response)
        return response