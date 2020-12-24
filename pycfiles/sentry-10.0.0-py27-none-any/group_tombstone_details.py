# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/group_tombstone_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.bases import ProjectEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.models import GroupHash, GroupTombstone

class GroupTombstoneDetailsEndpoint(ProjectEndpoint):

    def delete(self, request, project, tombstone_id):
        """
        Remove a GroupTombstone
        ```````````````````````

        Undiscards a group such that new events in that group will be captured.
        This does not restore any previous data.

        :pparam string organization_slug: the slug of the organization.
        :pparam string project_slug: the slug of the project to which this tombstone belongs.
        :pparam string tombstone_id: the ID of the tombstone to remove.
        :auth: required
        """
        try:
            tombstone = GroupTombstone.objects.get(project_id=project.id, id=tombstone_id)
        except GroupTombstone.DoesNotExist:
            raise ResourceDoesNotExist

        GroupHash.objects.filter(project_id=project.id, group_tombstone_id=tombstone_id).update(group_tombstone_id=None)
        tombstone.delete()
        return Response(status=204)