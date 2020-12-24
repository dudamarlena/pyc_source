# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/group_plugin_action.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import, division
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from sudo.utils import is_safe_url
from sentry.models import Group, GroupMeta
from sentry.plugins import plugins
from sentry.web.frontend.base import ProjectView

class GroupPluginActionView(ProjectView):
    required_scope = 'event:read'

    def handle(self, request, organization, project, group_id, slug):
        group = get_object_or_404(Group, pk=group_id, project=project)
        try:
            plugin = plugins.get(slug)
        except KeyError:
            raise Http404('Plugin not found')

        GroupMeta.objects.populate_cache([group])
        response = plugin.get_view_response(request, group)
        if response:
            return response
        redirect = request.META.get('HTTP_REFERER', '')
        if not is_safe_url(redirect, host=request.get_host()):
            redirect = ('/{}/{}/').format(organization.slug, group.project.slug)
        return HttpResponseRedirect(redirect)