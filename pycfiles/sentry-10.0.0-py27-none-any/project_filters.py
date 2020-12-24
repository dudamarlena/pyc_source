# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_filters.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry import message_filters
from sentry.api.bases.project import ProjectEndpoint

class ProjectFiltersEndpoint(ProjectEndpoint):

    def get(self, request, project):
        """
        List a project's filters

        Retrieve a list of filters for a given project.

            {method} {path}

        """
        results = []
        for flt in message_filters.get_all_filters():
            filter_spec = flt.spec
            results.append({'id': filter_spec.id, 
               'active': message_filters.get_filter_state(filter_spec.id, project), 
               'description': filter_spec.description, 
               'name': filter_spec.name, 
               'hello': filter_spec.id + ' - ' + filter_spec.name})

        results.sort(key=lambda x: x['name'])
        return Response(results)