# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/incidents/endpoints/bases.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.exceptions import PermissionDenied
from sentry import features
from sentry.api.bases.project import ProjectEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.incidents.models import AlertRule

class ProjectAlertRuleEndpoint(ProjectEndpoint):

    def convert_args(self, request, alert_rule_id, *args, **kwargs):
        args, kwargs = super(ProjectAlertRuleEndpoint, self).convert_args(request, *args, **kwargs)
        project = kwargs['project']
        if not features.has('organizations:incidents', project.organization, actor=request.user):
            raise ResourceDoesNotExist
        if not request.access.has_project_access(project):
            raise PermissionDenied
        try:
            kwargs['alert_rule'] = AlertRule.objects.get(project=project, id=alert_rule_id)
        except AlertRule.DoesNotExist:
            raise ResourceDoesNotExist

        return (args, kwargs)