# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/organization_integration_setup.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import, print_function
import logging
from django.http import Http404
from sentry.integrations.pipeline import IntegrationPipeline
from sentry.web.frontend.base import OrganizationView
logger = logging.getLogger('sentry.integrations')

class OrganizationIntegrationSetupView(OrganizationView):
    required_scope = 'org:integrations'
    csrf_protect = False

    def handle(self, request, organization, provider_id):
        pipeline = IntegrationPipeline(request=request, organization=organization, provider_key=provider_id)
        if not pipeline.provider.can_add:
            raise Http404
        pipeline.initialize()
        return pipeline.current_step()