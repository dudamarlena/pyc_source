# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/integrations/vsts/webhooks.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from .client import VstsApiClient
import logging, six
from sentry.models import Identity, Integration, OrganizationIntegration, sync_group_assignee_inbound
from sentry.models.apitoken import generate_token
from sentry.api.base import Endpoint
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import constant_time_compare
import re
UNSET = object()
EMAIL_PARSER = re.compile('<(.*)>')
logger = logging.getLogger('sentry.integrations')
PROVIDER_KEY = 'vsts'

class WorkItemWebhook(Endpoint):
    authentication_classes = ()
    permission_classes = ()

    def get_client(self, identity, oauth_redirect_url):
        return VstsApiClient(identity, oauth_redirect_url)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(WorkItemWebhook, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            event_type = data['eventType']
            external_id = data['resourceContainers']['collection']['id']
        except KeyError as e:
            logger.info('vsts.invalid-webhook-payload', extra={'error': six.text_type(e)})

        if event_type == 'workitem.updated':
            try:
                integration = Integration.objects.get(provider=PROVIDER_KEY, external_id=external_id)
            except Integration.DoesNotExist:
                logger.info('vsts.integration-in-webhook-payload-does-not-exist', extra={'external_id': external_id, 'event_type': event_type})

            try:
                self.check_webhook_secret(request, integration)
            except AssertionError:
                logger.info('vsts.invalid-webhook-secret', extra={'event_type': event_type, 'integration_id': integration.id})
                return self.respond(status=401)

            self.handle_updated_workitem(data, integration)
        return self.respond()

    def check_webhook_secret(self, request, integration):
        try:
            integration_secret = integration.metadata['subscription']['secret']
            webhook_payload_secret = request.META['HTTP_SHARED_SECRET']
        except KeyError as e:
            logger.info('vsts.missing-webhook-secret', extra={'error': six.text_type(e), 'integration_id': integration.id})

        assert constant_time_compare(integration_secret, webhook_payload_secret)

    def handle_updated_workitem(self, data, integration):
        try:
            external_issue_key = data['resource']['workItemId']
            project = data['resourceContainers']['project']['id']
        except KeyError as e:
            logger.info('vsts.updating-workitem-does-not-have-necessary-information', extra={'error': six.text_type(e), 'integration_id': integration.id})

        try:
            assigned_to = data['resource']['fields'].get('System.AssignedTo')
            status_change = data['resource']['fields'].get('System.State')
        except KeyError as e:
            logger.info('vsts.updated-workitem-fields-not-passed', extra={'error': six.text_type(e), 
               'workItemId': data['resource']['workItemId'], 
               'integration_id': integration.id})
            return

        self.handle_assign_to(integration, external_issue_key, assigned_to)
        self.handle_status_change(integration, external_issue_key, status_change, project)

    def handle_assign_to(self, integration, external_issue_key, assigned_to):
        if not assigned_to:
            return
        else:
            new_value = assigned_to.get('newValue')
            if new_value is not None:
                try:
                    email = self.parse_email(new_value)
                except AttributeError as e:
                    logger.info('vsts.failed-to-parse-email-in-handle-assign-to', extra={'error': six.text_type(e), 
                       'integration_id': integration.id, 
                       'assigned_to_values': assigned_to, 
                       'external_issue_key': external_issue_key})
                    return

                assign = True
            else:
                email = None
                assign = False
            sync_group_assignee_inbound(integration=integration, email=email, external_issue_key=external_issue_key, assign=assign)
            return

    def handle_status_change(self, integration, external_issue_key, status_change, project):
        if status_change is None:
            return
        else:
            organization_ids = OrganizationIntegration.objects.filter(integration_id=integration.id).values_list('organization_id', flat=True)
            for organization_id in organization_ids:
                installation = integration.get_installation(organization_id)
                data = {'new_state': status_change['newValue'], 
                   'old_state': status_change.get('oldValue'), 
                   'project': project}
                installation.sync_status_inbound(external_issue_key, data)

            return

    def parse_email(self, email):
        return EMAIL_PARSER.search(email).group(1)

    def create_subscription(self, instance, identity_data, oauth_redirect_url):
        client = self.get_client(Identity(data=identity_data), oauth_redirect_url)
        shared_secret = generate_token()
        return (client.create_subscription(instance, shared_secret), shared_secret)