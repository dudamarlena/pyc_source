# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/internal_packages.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import pkg_resources
from rest_framework.response import Response
from sentry.api.base import Endpoint
from sentry.plugins import plugins
from sentry.api.permissions import SuperuserPermission

class InternalPackagesEndpoint(Endpoint):
    permission_classes = (
     SuperuserPermission,)

    def get(self, request):
        data = {'modules': sorted([ (p.project_name, p.version) for p in pkg_resources.working_set ]), 
           'extensions': [ (p.get_title(), '%s.%s' % (p.__module__, p.__class__.__name__)) for p in plugins.all(version=None)
                       ]}
        return Response(data)