# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/organization_access_request.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from sentry.api.serializers import Serializer, register, serialize
from sentry.models import OrganizationAccessRequest

@register(OrganizationAccessRequest)
class OrganizationAccessRequestSerializer(Serializer):

    def serialize(self, obj, attrs, user):
        d = {'id': six.text_type(obj.id), 
           'member': serialize(obj.member), 
           'team': serialize(obj.team)}
        return d