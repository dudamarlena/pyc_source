# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_tagkey_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry import tagstore
from sentry.api.base import EnvironmentMixin
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.api.serializers import serialize
from sentry.constants import PROTECTED_TAG_KEYS
from sentry.models import AuditLogEntryEvent, Environment

class ProjectTagKeyDetailsEndpoint(ProjectEndpoint, EnvironmentMixin):

    def get(self, request, project, key):
        lookup_key = tagstore.prefix_reserved_key(key)
        try:
            environment_id = self._get_environment_id_from_request(request, project.organization_id)
        except Environment.DoesNotExist:
            raise ResourceDoesNotExist

        try:
            tagkey = tagstore.get_tag_key(project.id, environment_id, lookup_key)
        except tagstore.TagKeyNotFound:
            raise ResourceDoesNotExist

        return Response(serialize(tagkey, request.user))

    def delete(self, request, project, key):
        """
        Remove all occurrences of the given tag key.

            {method} {path}

        """
        if key in PROTECTED_TAG_KEYS:
            return Response(status=403)
        else:
            lookup_key = tagstore.prefix_reserved_key(key)
            try:
                from sentry import eventstream
                eventstream_state = eventstream.start_delete_tag(project.id, key)
                deleted = tagstore.delete_tag_key(project.id, lookup_key)
                eventstream.end_delete_tag(eventstream_state)
            except tagstore.TagKeyNotFound:
                raise ResourceDoesNotExist

            for tagkey in deleted:
                self.create_audit_entry(request=request, organization=project.organization, target_object=getattr(tagkey, 'id', None), event=AuditLogEntryEvent.TAGKEY_REMOVE, data=tagkey.get_audit_log_data())

            return Response(status=204)