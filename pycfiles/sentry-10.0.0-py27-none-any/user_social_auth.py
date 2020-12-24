# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/user_social_auth.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from django.conf import settings
from social_auth.models import UserSocialAuth
from sentry.api.serializers import Serializer, register

@register(UserSocialAuth)
class UserSocialAuthSerializer(Serializer):

    def serialize(self, obj, attrs, user):
        return {'id': six.text_type(obj.id), 
           'provider': obj.provider, 
           'providerLabel': settings.AUTH_PROVIDER_LABELS[obj.provider]}