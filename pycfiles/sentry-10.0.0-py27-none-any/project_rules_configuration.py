# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_rules_configuration.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.bases.project import ProjectEndpoint, StrictProjectPermission
from sentry.rules import rules
from rest_framework.response import Response

class ProjectRulesConfigurationEndpoint(ProjectEndpoint):
    permission_classes = (
     StrictProjectPermission,)

    def get(self, request, project):
        """
        Retrieve the list of configuration options for a given project.
        """
        action_list = []
        condition_list = []
        for rule_type, rule_cls in rules:
            node = rule_cls(project)
            context = {'id': node.id, 'label': node.label, 'enabled': node.is_enabled()}
            if hasattr(node, 'form_fields'):
                context['formFields'] = node.form_fields
            if rule_type.startswith('condition/'):
                condition_list.append(context)
            elif rule_type.startswith('action/'):
                action_list.append(context)

        context = {'actions': action_list, 'conditions': condition_list}
        return Response(context)