# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/integrations/slack/action_endpoint.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry import analytics
from sentry import http
from sentry.api import client
from sentry.api.base import Endpoint
from sentry.models import Group, Project, Identity, IdentityProvider, ApiKey
from sentry.utils import json
from .link_identity import build_linking_url
from .requests import SlackActionRequest, SlackRequestError
from .utils import build_group_attachment, logger
LINK_IDENTITY_MESSAGE = "Looks like you haven't linked your Sentry account with your Slack identity yet! <{associate_url}|Link your identity now> to perform actions in Sentry through Slack."
RESOLVE_SELECTOR = {'label': 'Resolve issue', 
   'type': 'select', 
   'name': 'resolve_type', 
   'placeholder': 'Select the resolution target', 
   'value': 'resolved', 
   'options': [{'label': 'Immediately', 'value': 'resolved'}, {'label': 'In the next release', 'value': 'resolved:inNextRelease'}, {'label': 'In the current release', 'value': 'resolved:inCurrentRelease'}]}

class SlackActionEndpoint(Endpoint):
    authentication_classes = ()
    permission_classes = ()

    def api_error(self, error):
        logger.info('slack.action.api-error', extra={'response': error.body})
        return self.respond({'response_type': 'ephemeral', 
           'replace_original': False, 
           'text': "Sentry can't perform that action right now on your behalf!"})

    def on_assign(self, request, identity, group, action):
        assignee = action['selected_options'][0]['value']
        if assignee == 'none':
            assignee = None
        self.update_group(group, identity, {'assignedTo': assignee})
        analytics.record('integrations.slack.assign', actor_id=identity.user_id)
        return

    def on_status(self, request, identity, group, action, data, integration):
        status = action['value']
        status_data = status.split(':', 1)
        status = {'status': status_data[0]}
        resolve_type = status_data[(-1)]
        if resolve_type == 'inNextRelease':
            status.update({'statusDetails': {'inNextRelease': True}})
        elif resolve_type == 'inCurrentRelease':
            status.update({'statusDetails': {'inRelease': 'latest'}})
        self.update_group(group, identity, status)
        analytics.record('integrations.slack.status', status=status['status'], resolve_type=resolve_type, actor_id=identity.user_id)

    def update_group(self, group, identity, data):
        event_write_key = ApiKey(organization=group.project.organization, scope_list=['event:write'])
        return client.put(path=('/projects/{}/{}/issues/').format(group.project.organization.slug, group.project.slug), params={'id': group.id}, data=data, user=identity.user, auth=event_write_key)

    def open_resolve_dialog(self, data, group, integration):
        callback_id = json.dumps({'issue': group.id, 
           'orig_response_url': data['response_url'], 
           'is_message': self.is_message(data)})
        dialog = {'callback_id': callback_id, 
           'title': 'Resolve Issue', 
           'submit_label': 'Resolve', 
           'elements': [
                      RESOLVE_SELECTOR]}
        payload = {'dialog': json.dumps(dialog), 
           'trigger_id': data['trigger_id'], 
           'token': integration.metadata['access_token']}
        session = http.build_session()
        req = session.post('https://slack.com/api/dialog.open', data=payload)
        resp = req.json()
        if not resp.get('ok'):
            logger.error('slack.action.response-error', extra={'response': resp})

    def construct_reply(self, attachment, is_message=False):
        if is_message:
            attachment = {'attachments': [attachment]}
        return attachment

    def is_message(self, data):
        return data.get('original_message', {}).get('type') == 'message'

    def post(self, request):
        logging_data = {}
        try:
            slack_request = SlackActionRequest(request)
            slack_request.validate()
        except SlackRequestError as e:
            return self.respond(status=e.status)

        data = slack_request.data
        channel_id = data.get('channel', {}).get('id')
        user_id = data.get('user', {}).get('id')
        integration = slack_request.integration
        logging_data['integration_id'] = integration.id
        group_id = slack_request.callback_data['issue']
        action_list = data.get('actions', [])
        try:
            group = Group.objects.select_related('project__organization').get(project__in=Project.objects.filter(organization__in=integration.organizations.all()), id=group_id)
        except Group.DoesNotExist:
            logger.error('slack.action.invalid-issue', extra=logging_data)
            return self.respond(status=403)

        try:
            idp = IdentityProvider.objects.get(type='slack', external_id=slack_request.team_id)
        except IdentityProvider.DoesNotExist:
            logger.error('slack.action.invalid-team-id', extra=logging_data)
            return self.respond(status=403)

        try:
            identity = Identity.objects.get(idp=idp, external_id=user_id)
        except Identity.DoesNotExist:
            associate_url = build_linking_url(integration, group.organization, user_id, channel_id, data.get('response_url'))
            return self.respond({'response_type': 'ephemeral', 
               'replace_original': False, 
               'text': LINK_IDENTITY_MESSAGE.format(associate_url=associate_url)})

        if slack_request.type == 'dialog_submission' and 'resolve_type' in data['submission']:
            action = {'name': 'status', 'value': data['submission']['resolve_type']}
            try:
                self.on_status(request, identity, group, action, data, integration)
            except client.ApiError as e:
                return self.api_error(e)

            group = Group.objects.get(id=group.id)
            attachment = build_group_attachment(group, identity=identity, actions=[action])
            body = self.construct_reply(attachment, is_message=slack_request.callback_data['is_message'])
            session = http.build_session()
            req = session.post(slack_request.callback_data['orig_response_url'], json=body)
            resp = req.json()
            if not resp.get('ok'):
                logger.error('slack.action.response-error', extra={'response': resp})
            return self.respond()
        defer_attachment_update = False
        try:
            for action in action_list:
                action_type = action['name']
                if action_type == 'status':
                    self.on_status(request, identity, group, action, data, integration)
                elif action_type == 'assign':
                    self.on_assign(request, identity, group, action)
                elif action_type == 'resolve_dialog':
                    self.open_resolve_dialog(data, group, integration)
                    defer_attachment_update = True

        except client.ApiError as e:
            return self.api_error(e)

        if defer_attachment_update:
            return self.respond()
        group = Group.objects.get(id=group.id)
        attachment = build_group_attachment(group, identity=identity, actions=action_list)
        body = self.construct_reply(attachment, is_message=self.is_message(data))
        return self.respond(body)