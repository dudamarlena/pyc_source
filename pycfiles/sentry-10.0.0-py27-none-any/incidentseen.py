# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/incidentseen.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from sentry.api.serializers import Serializer, register, serialize
from sentry.incidents.models import IncidentSeen
from sentry.utils.db import attach_foreignkey

@register(IncidentSeen)
class IncidentSeenSerializer(Serializer):

    def get_attrs(self, item_list, user):
        attach_foreignkey(item_list, IncidentSeen.user)
        user_map = {d['id']:d for d in serialize(set(i.user for i in item_list), user)}
        result = {}
        for item in item_list:
            result[item] = {'user': user_map[six.text_type(item.user_id)]}

        return result

    def serialize(self, obj, attrs, user):
        data = attrs['user']
        data['lastSeen'] = obj.last_seen
        return data