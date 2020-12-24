# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/vsts_extension_configuration.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.core.urlresolvers import reverse
from django.utils.http import urlencode
from sentry.integrations.pipeline import IntegrationPipeline
from sentry.models import Organization
from sentry.web.frontend.base import BaseView

class VstsExtensionConfigurationView(BaseView):
    auth_required = False

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            configure_uri = ('{}?{}').format(reverse('vsts-extension-configuration'), urlencode({'targetId': request.GET['targetId'], 'targetName': request.GET['targetName']}))
            redirect_uri = ('{}?{}').format(reverse('sentry-login'), urlencode({'next': configure_uri}))
            return self.redirect(redirect_uri)
        else:
            if request.user.get_orgs().count() == 1:
                org = request.user.get_orgs()[0]
                pipeline = self.init_pipeline(request, org, request.GET['targetId'], request.GET['targetName'])
                return pipeline.current_step()
            return self.redirect(('/extensions/vsts/link/?{}').format(urlencode({'targetId': request.GET['targetId'], 
               'targetName': request.GET['targetName']})))

    def post(self, request, *args, **kwargs):
        org = Organization.objects.get(slug=request.POST['organization'])
        pipeline = self.init_pipeline(request, org, request.POST['vsts_id'], request.POST['vsts_name'])
        return pipeline.current_step()

    def init_pipeline(self, request, organization, id, name):
        pipeline = IntegrationPipeline(request=request, organization=organization, provider_key='vsts-extension')
        pipeline.initialize()
        pipeline.bind_state('vsts', {'accountId': id, 'accountName': name})
        return pipeline