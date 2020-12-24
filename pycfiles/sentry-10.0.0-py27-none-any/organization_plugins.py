# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_plugins.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.plugins import plugins
from sentry.api.bases.organization import OrganizationEndpoint
from sentry.api.serializers import serialize
from sentry.api.serializers.models.organization_plugin import OrganizationPluginSerializer
from sentry.api.serializers.models.plugin import PluginSerializer
from sentry.models import ProjectOption

class OrganizationPluginsEndpoint(OrganizationEndpoint):

    def get(self, request, organization):
        all_plugins = dict([ (p.slug, p) for p in plugins.all() ])
        if 'plugins' in request.GET:
            if request.GET.get('plugins') == '_all':
                return Response(serialize([ p for p in plugins.all() ], request.user, PluginSerializer()))
            desired_plugins = set(request.GET.getlist('plugins'))
        else:
            desired_plugins = set(all_plugins.keys())
        desired_plugins = desired_plugins & set(all_plugins.keys())
        enabled_plugins = ProjectOption.objects.filter(key__in=[ '%s:enabled' % slug for slug in desired_plugins ], project__organization=organization).select_related('project')
        resources = []
        for project_option in enabled_plugins:
            resources.append(serialize(all_plugins[project_option.key.split(':')[0]], request.user, OrganizationPluginSerializer(project_option.project)))

        return Response(resources)