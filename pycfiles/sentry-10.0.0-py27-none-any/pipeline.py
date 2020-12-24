# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/integrations/pipeline.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
__all__ = ['IntegrationPipeline']
from django.db import IntegrityError
from django.utils import timezone
from django.utils.translation import ugettext as _
from sentry.api.serializers import serialize
from sentry.constants import ObjectStatus
from sentry.integrations.exceptions import IntegrationError
from sentry.models import Identity, IdentityProvider, IdentityStatus, Integration
from sentry.pipeline import Pipeline
from sentry.web.helpers import render_to_response
from . import default_manager
import six

def ensure_integration(key, data):
    defaults = {'metadata': data.get('metadata', {}), 
       'name': data.get('name', data['external_id']), 
       'status': ObjectStatus.VISIBLE}
    integration, created = Integration.objects.get_or_create(provider=key, external_id=data['external_id'], defaults=defaults)
    if not created:
        integration.update(**defaults)
    return integration


class IntegrationPipeline(Pipeline):
    pipeline_name = 'integration_pipeline'
    provider_manager = default_manager

    def finish_pipeline(self):
        try:
            data = self.provider.build_integration(self.state.data)
        except IntegrationError as e:
            self.get_logger().info('build-integration.failure', extra={'error_message': six.text_type(e), 
               'error_status': getattr(e, 'code', None), 
               'provider_key': self.provider.key})
            return self.error(e.message)

        response = self._finish_pipeline(data)
        self.provider.post_install(self.integration, self.organization)
        self.clear_session()
        return response

    def _finish_pipeline(self, data):
        if 'reinstall_id' in data:
            self.integration = Integration.objects.get(provider=self.provider.integration_key, id=data['reinstall_id'])
            self.integration.update(external_id=data['external_id'], status=ObjectStatus.VISIBLE)
            self.integration.get_installation(self.organization.id).reinstall()
        elif 'expect_exists' in data:
            self.integration = Integration.objects.get(provider=self.provider.integration_key, external_id=data['external_id'])
        else:
            self.integration = ensure_integration(self.provider.integration_key, data)
        identity = data.get('user_identity')
        if identity:
            idp_external_id = data.get('idp_external_id', data['external_id'])
            idp_config = data.get('idp_config', {})
            idp, created = IdentityProvider.objects.get_or_create(external_id=idp_external_id, type=identity['type'], defaults={'config': idp_config})
            if not created:
                idp.update(config=idp_config)
            identity_data = {'status': IdentityStatus.VALID, 
               'scopes': identity['scopes'], 
               'data': identity['data'], 
               'date_verified': timezone.now()}
            try:
                identity_model, created = Identity.objects.get_or_create(idp=idp, user=self.request.user, external_id=identity['external_id'], defaults=identity_data)
                if not created:
                    identity_model.update(**identity_data)
            except IntegrityError:
                if idp.type in ('github', 'vsts'):
                    try:
                        other_identity = Identity.objects.get(idp=idp, external_id=identity['external_id'])
                    except Identity.DoesNotExist:
                        pass
                    else:
                        if not other_identity.user.has_usable_password():
                            proper_name = 'GitHub' if idp.type == 'github' else 'Azure DevOps'
                            return self._dialog_response({'error': _('The provided %s account is linked to a different Sentry user. To continue linking the current Sentry user, please use a different %s account.') % (
                                       proper_name, proper_name)}, False)

                identity_model = Identity.reattach(idp, identity['external_id'], self.request.user, identity_data)

        default_auth_id = None
        if self.provider.needs_default_identity:
            if not (identity and identity_model):
                raise NotImplementedError('Integration requires an identity')
            default_auth_id = identity_model.id
        org_integration = self.integration.add_organization(self.organization, self.request.user, default_auth_id=default_auth_id)
        return self._dialog_response(serialize(org_integration, self.request.user), True)

    def _dialog_response(self, data, success):
        context = {'payload': {'success': success, 'data': data}}
        return render_to_response('sentry/integrations/dialog-complete.html', context, self.request)