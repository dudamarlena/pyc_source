# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_plugins.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.plugins import plugins
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.serializers import serialize
from sentry.api.serializers.models.plugin import PluginSerializer

class ProjectPluginsEndpoint(ProjectEndpoint):

    def get(self, request, project):
        context = serialize([ plugin for plugin in plugins.configurable_for_project(project, version=None) ], request.user, PluginSerializer(project))
        return Response(context)