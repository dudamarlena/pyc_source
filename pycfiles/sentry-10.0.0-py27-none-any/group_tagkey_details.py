# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/group_tagkey_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry import tagstore
from sentry.api.base import DocSection, EnvironmentMixin
from sentry.api.bases.group import GroupEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.api.serializers import serialize
from sentry.models import Environment, Group
from sentry.utils.apidocs import scenario

@scenario('ListTagDetails')
def list_tag_details_scenario(runner):
    group = Group.objects.filter(project=runner.default_project).first()
    runner.request(method='GET', path='/issues/%s/tags/%s/' % (group.id, 'browser'))


class GroupTagKeyDetailsEndpoint(GroupEndpoint, EnvironmentMixin):
    doc_section = DocSection.EVENTS

    def get(self, request, group, key):
        """
        Retrieve Tag Details
        ````````````````````

        Returns details for given tag key related to an issue.

        :pparam string issue_id: the ID of the issue to retrieve.
        :pparam string key: the tag key to look the values up for.
        :auth: required
        """
        lookup_key = tagstore.prefix_reserved_key(key)
        try:
            environment_id = self._get_environment_id_from_request(request, group.project.organization_id)
        except Environment.DoesNotExist:
            raise ResourceDoesNotExist

        try:
            group_tag_key = tagstore.get_group_tag_key(group.project_id, group.id, environment_id, lookup_key)
        except tagstore.GroupTagKeyNotFound:
            raise ResourceDoesNotExist

        if group_tag_key.count is None:
            group_tag_key.count = tagstore.get_group_tag_value_count(group.project_id, group.id, environment_id, lookup_key)
        if group_tag_key.top_values is None:
            group_tag_key.top_values = tagstore.get_top_group_tag_values(group.project_id, group.id, environment_id, lookup_key)
        return Response(serialize(group_tag_key, request.user))