# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_tags.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry import tagstore
from sentry.api.base import EnvironmentMixin
from sentry.api.bases.project import ProjectEndpoint
from sentry.constants import PROTECTED_TAG_KEYS
from sentry.models import Environment

class ProjectTagsEndpoint(ProjectEndpoint, EnvironmentMixin):

    def get(self, request, project):
        try:
            environment_id = self._get_environment_id_from_request(request, project.organization_id)
        except Environment.DoesNotExist:
            tag_keys = []
        else:
            tag_keys = sorted(tagstore.get_tag_keys(project.id, environment_id, include_values_seen=True), key=lambda x: x.key)

        data = []
        for tag_key in tag_keys:
            data.append({'key': tagstore.get_standardized_key(tag_key.key), 
               'name': tagstore.get_tag_key_label(tag_key.key), 
               'uniqueValues': tag_key.values_seen, 
               'canDelete': tag_key.key not in PROTECTED_TAG_KEYS})

        return Response(data)