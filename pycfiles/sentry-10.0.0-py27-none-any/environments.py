# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/helpers/environments.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.models import Environment
environment_visibility_filter_options = {'all': lambda queryset: queryset, 
   'hidden': lambda queryset: queryset.filter(is_hidden=True), 
   'visible': lambda queryset: queryset.exclude(is_hidden=True)}

def get_environments(request, organization):
    requested_environments = set(request.GET.getlist('environment'))
    if not requested_environments:
        return []
    environments = list(Environment.objects.filter(organization_id=organization.id, name__in=requested_environments))
    if set(requested_environments) != set([ e.name for e in environments ]):
        raise ResourceDoesNotExist
    return environments