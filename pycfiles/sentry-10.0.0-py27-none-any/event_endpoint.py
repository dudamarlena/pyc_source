# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/integrations/slack/event_endpoint.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import json, re, six
from collections import defaultdict
from django.conf import settings
from django.db.models import Q
from sentry import http
from sentry.api.base import Endpoint
from sentry.incidents.models import Incident
from sentry.models import Group, Project
from .requests import SlackEventRequest, SlackRequestError
from .utils import build_group_attachment, build_incident_attachment, logger
_link_regexp = re.compile('^https?\\://[^/]+/[^/]+/[^/]+/(issues|incidents)/(\\d+)')
_org_slug_regexp = re.compile('^https?\\://[^/]+/organizations/([^/]+)/')

def unfurl_issues(integration, issue_map):
    results = {g.id:g for g in Group.objects.filter(id__in=set(issue_map.keys()), project__in=Project.objects.filter(organization__in=integration.organizations.all()))}
    if not results:
        return {}
    return {v:build_group_attachment(results[k]) for k, v in six.iteritems(issue_map) if k in results}


def unfurl_incidents(integration, incident_map):
    filter_query = Q()
    for identifier, url in six.iteritems(incident_map):
        org_slug = _org_slug_regexp.match(url).group(1)
        filter_query |= Q(identifier=identifier, organization__slug=org_slug)

    results = {i.identifier:i for i in Incident.objects.filter(filter_query, organization__in=integration.organizations.all())}
    if not results:
        return {}
    return {v:build_incident_attachment(results[k]) for k, v in six.iteritems(incident_map) if k in results}


class SlackEventEndpoint(Endpoint):
    event_handlers = {'issues': unfurl_issues, 'incidents': unfurl_incidents}
    authentication_classes = ()
    permission_classes = ()

    def _parse_url(self, link):
        """
        Extracts event type and id from a url.
        :param link: Url to parse to information from
        :return: If successful, a tuple containing the event_type and id. If we
        were unsuccessful at matching, a tuple containing two None values
        """
        match = _link_regexp.match(link)
        if not match:
            return (None, None)
        else:
            try:
                return (
                 match.group(1), int(match.group(2)))
            except (TypeError, ValueError):
                return (None, None)

            return

    def on_url_verification(self, request, data):
        return self.respond({'challenge': data['challenge']})

    def on_link_shared(self, request, integration, token, data):
        parsed_events = defaultdict(dict)
        for item in data['links']:
            event_type, instance_id = self._parse_url(item['url'])
            if not instance_id:
                continue
            parsed_events[event_type][instance_id] = item['url']

        if not parsed_events:
            return
        results = {}
        for event_type, instance_map in parsed_events.items():
            results.update(self.event_handlers[event_type](integration, instance_map))

        if not results:
            return
        if settings.SLACK_INTEGRATION_USE_WST:
            access_token = integration.metadata['access_token']
        else:
            access_token = integration.metadata['user_access_token']
        payload = {'token': access_token, 
           'channel': data['channel'], 
           'ts': data['message_ts'], 
           'unfurls': json.dumps(results)}
        session = http.build_session()
        req = session.post('https://slack.com/api/chat.unfurl', data=payload)
        req.raise_for_status()
        resp = req.json()
        if not resp.get('ok'):
            logger.error('slack.event.unfurl-error', extra={'response': resp})
        return self.respond()

    def post(self, request):
        try:
            slack_request = SlackEventRequest(request)
            slack_request.validate()
        except SlackRequestError as e:
            return self.respond(status=e.status)

        if slack_request.is_challenge():
            return self.on_url_verification(request, slack_request.data)
        if slack_request.type == 'link_shared':
            resp = self.on_link_shared(request, slack_request.integration, slack_request.data.get('token'), slack_request.data.get('event'))
            if resp:
                return resp
        return self.respond()