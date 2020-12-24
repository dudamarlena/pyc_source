# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/group_tags.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry import tagstore
from sentry.api.bases.group import GroupEndpoint
from sentry.api.helpers.environments import get_environments
from sentry.api.serializers import serialize

class GroupTagsEndpoint(GroupEndpoint):

    def get(self, request, group):
        keys = [ tagstore.prefix_reserved_key(k) for k in request.GET.getlist('key') if k ] or None
        if keys:
            value_limit = 9
        else:
            value_limit = 10
        environment_ids = [ e.id for e in get_environments(request, group.project.organization) ]
        tag_keys = tagstore.get_group_tag_keys_and_top_values(group.project_id, group.id, environment_ids, keys=keys, value_limit=value_limit)
        return Response(serialize(tag_keys, request.user))