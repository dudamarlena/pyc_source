# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/group_tombstone.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.paginator import OffsetPaginator
from sentry.api.serializers import serialize
from sentry.models import GroupTombstone

class GroupTombstoneEndpoint(ProjectEndpoint):

    def get(self, request, project):
        """
        Retrieve a Project's GroupTombstones
        ````````````````````````````````````

        Lists a project's `GroupTombstone` objects

        :pparam string organization_id: the ID of the organization.
        :pparam string project_id: the ID of the project to get the tombstones for
        :auth: required
        """
        queryset = GroupTombstone.objects.filter(project=project)
        return self.paginate(request=request, queryset=queryset, order_by='id', paginator_cls=OffsetPaginator, on_results=lambda x: serialize(x, request.user))