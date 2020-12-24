# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/auth_provider.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from django.db.models import F
from sentry.api.serializers import Serializer, register
from sentry.models import AuthProvider, OrganizationMember
from sentry.utils.http import absolute_uri

@register(AuthProvider)
class AuthProviderSerializer(Serializer):

    def serialize(self, obj, attrs, user):
        organization = obj.organization
        pending_links_count = OrganizationMember.objects.filter(organization=organization, flags=F('flags').bitand(~OrganizationMember.flags['sso:linked'])).count()
        login_url = organization.get_url()
        return {'id': six.text_type(obj.id), 
           'provider_name': obj.provider, 
           'pending_links_count': pending_links_count, 
           'login_url': absolute_uri(login_url), 
           'default_role': organization.default_role, 
           'require_link': not obj.flags.allow_unlinked}