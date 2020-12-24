# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/pipeline_advancer.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import, print_function
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from sentry.identity.pipeline import IdentityProviderPipeline
from sentry.integrations.pipeline import IntegrationPipeline
from sentry.web.frontend.base import BaseView
PIPELINE_CLASSES = [
 IntegrationPipeline, IdentityProviderPipeline]
FORWARD_INSTALL_FOR = [
 'github']

class PipelineAdvancerView(BaseView):
    """Gets the current pipeline from the request and executes the current step."""
    auth_required = False
    csrf_protect = False

    def handle(self, request, provider_id):
        pipeline = None
        for pipeline_cls in PIPELINE_CLASSES:
            pipeline = pipeline_cls.get_for_request(request=request)
            if pipeline:
                break

        if provider_id in FORWARD_INSTALL_FOR and request.GET.get('setup_action') == 'install' and pipeline is None:
            installation_id = request.GET.get('installation_id')
            return self.redirect(reverse('integration-installation', args=[provider_id, installation_id]))
        else:
            if pipeline is None or not pipeline.is_valid():
                messages.add_message(request, messages.ERROR, _('Invalid request.'))
                return self.redirect('/')
            return pipeline.current_step()