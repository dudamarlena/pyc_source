# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/group_similar_issues.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import functools
from rest_framework.response import Response
from sentry.api.bases.group import GroupEndpoint
from sentry.api.serializers import serialize
from sentry.models import Group
from sentry.similarity import features
from sentry.utils.functional import apply_values

class GroupSimilarIssuesEndpoint(GroupEndpoint):

    def get(self, request, group):
        limit = request.GET.get('limit', None)
        if limit is not None:
            limit = int(limit) + 1
        results = filter(lambda group_id__scores: group_id__scores[0] != group.id, features.compare(group, limit=limit))
        serialized_groups = apply_values(functools.partial(serialize, user=request.user), Group.objects.in_bulk([ group_id for group_id, scores in results ]))
        return Response(filter(lambda group_id__scores: group_id__scores[0] is not None, map(lambda group_id__scores: (
         serialized_groups.get(group_id__scores[0]),
         group_id__scores[1]), results)))