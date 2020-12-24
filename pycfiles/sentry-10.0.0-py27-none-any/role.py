# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/role.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from sentry.api.serializers import Serializer

class RoleSerializer(Serializer):

    def serialize(self, obj, attrs, user, **kwargs):
        allowed_roles = kwargs.get('allowed_roles') or []
        return {'id': six.text_type(obj.id), 
           'name': obj.name, 
           'desc': obj.desc, 
           'scopes': obj.scopes, 
           'is_global': obj.is_global, 
           'allowed': obj in allowed_roles}