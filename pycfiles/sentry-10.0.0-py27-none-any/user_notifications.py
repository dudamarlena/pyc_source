# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/user_notifications.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from collections import defaultdict
from sentry.api.serializers import Serializer
from sentry.models import UserOption

class UserNotificationsSerializer(Serializer):

    def get_attrs(self, item_list, user, **kwargs):
        notification_option_key = kwargs['notification_option_key']
        filter_args = {}
        if notification_option_key in ('alerts', 'workflow', 'email'):
            filter_args['project__isnull'] = False
        else:
            if notification_option_key == 'deploy':
                filter_args['organization__isnull'] = False
            data = list(UserOption.objects.filter(key=notification_option_key, user__in=item_list, **filter_args).select_related('user', 'project', 'organization'))
            results = defaultdict(list)
            for uo in data:
                results[uo.user].append(uo)

        return results

    def serialize(self, obj, attrs, user, **kwargs):
        notification_option_key = kwargs['notification_option_key']
        data = {}
        for uo in attrs:
            if notification_option_key == 'reports:disabled-organizations':
                for org_id in uo.value:
                    data[org_id] = 0

            elif uo.project is not None:
                data[uo.project.id] = uo.value
            elif uo.organization is not None:
                data[uo.organization.id] = uo.value

        return data