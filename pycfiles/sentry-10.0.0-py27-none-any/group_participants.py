# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/group_participants.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases import GroupEndpoint
from sentry.api.serializers import serialize
from sentry.models import User

class GroupParticipantsEndpoint(GroupEndpoint):

    def get(self, request, group):
        participants = list(User.objects.filter(groupsubscription__is_active=True, groupsubscription__group=group))
        return Response(serialize(participants, request.user))