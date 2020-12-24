# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/integrations/slack/link_identity.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import Http404
from django.utils import timezone
from django.views.decorators.cache import never_cache
from sentry import http
from sentry.models import Integration, Identity, IdentityProvider, IdentityStatus, Organization
from sentry.utils.http import absolute_uri
from sentry.utils.signing import sign, unsign
from sentry.web.frontend.base import BaseView
from sentry.web.helpers import render_to_response
from .utils import logger

def build_linking_url(integration, organization, slack_id, channel_id, response_url):
    signed_params = sign(integration_id=integration.id, organization_id=organization.id, slack_id=slack_id, channel_id=channel_id, response_url=response_url)
    return absolute_uri(reverse('sentry-integration-slack-link-identity', kwargs={'signed_params': signed_params}))


class SlackLinkIdentitiyView(BaseView):

    @never_cache
    def handle(self, request, signed_params):
        params = unsign(signed_params.encode('ascii', errors='ignore'))
        try:
            organization = Organization.objects.get(id__in=request.user.get_orgs(), id=params['organization_id'])
        except Organization.DoesNotExist:
            raise Http404

        try:
            integration = Integration.objects.get(id=params['integration_id'], organizations=organization)
        except Integration.DoesNotExist:
            raise Http404

        try:
            idp = IdentityProvider.objects.get(external_id=integration.external_id, type='slack')
        except IdentityProvider.DoesNotExist:
            raise Http404

        if request.method != 'POST':
            return render_to_response('sentry/auth-link-identity.html', request=request, context={'organization': organization, 'provider': integration.get_provider()})
        defaults = {'status': IdentityStatus.VALID, 'date_verified': timezone.now()}
        try:
            identity, created = Identity.objects.get_or_create(idp=idp, user=request.user, external_id=params['slack_id'], defaults=defaults)
            if not created:
                identity.update(**defaults)
        except IntegrityError:
            Identity.reattach(idp, params['slack_id'], request.user, defaults)

        payload = {'replace_original': False, 
           'response_type': 'ephemeral', 
           'text': "Your Slack identity has been linked to your Sentry account. You're good to go!"}
        session = http.build_session()
        req = session.post(params['response_url'], json=payload)
        resp = req.json()
        if not resp.get('ok') and resp.get('error') != 'Expired url':
            logger.error('slack.link-notify.response-error', extra={'response': resp})
        return render_to_response('sentry/slack-linked.html', request=request, context={'channel_id': params['channel_id'], 'team_id': integration.external_id})