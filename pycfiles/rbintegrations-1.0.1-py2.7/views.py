# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbintegrations/trello/views.py
# Compiled at: 2020-01-07 04:31:42
"""Views for the Trello integration."""
from __future__ import unicode_literals
import json, logging
from django.http import HttpResponse
from django.utils.six.moves.urllib.parse import urlencode
from django.utils.six.moves.urllib.request import urlopen
from django.views.generic import View
from reviewboard.integrations.base import get_integration_manager
from reviewboard.reviews.views import ReviewRequestViewMixin
logger = logging.getLogger(__name__)

class TrelloCardSearchView(ReviewRequestViewMixin, View):
    """The view to search for Trello cards (for use with auto-complete)."""

    def get(self, request, **kwargs):
        """Perform a search for cards.

        Args:
            request (django.http.HttpRequest):
                The request.

            **kwargs (dict):
                Additional keyword arguments.

        Returns:
            django.http.HttpResponse:
            A response containing JSON with a list of cards matching the
            search criteria.
        """
        from rbintegrations.trello.integration import TrelloIntegration
        integration_manager = get_integration_manager()
        integration = integration_manager.get_integration(TrelloIntegration.integration_id)
        configs = (config for config in integration.get_configs(self.review_request.local_site) if config.match_conditions(form_cls=integration.config_form_cls, review_request=self.review_request))
        results = []
        params = {b'card_board': b'true', 
           b'card_fields': b'id,name,shortUrl', 
           b'card_list': b'true', 
           b'cards_limit': 20, 
           b'modelTypes': b'cards', 
           b'partial': b'true', 
           b'query': request.GET.get(b'q')}
        for config in configs:
            params[b'key'] = config.settings[b'trello_api_key']
            params[b'token'] = config.settings[b'trello_api_token']
            url = b'https://api.trello.com/1/search?%s' % urlencode(params)
            try:
                response = urlopen(url)
                data = json.loads(response.read())
                for card in data[b'cards']:
                    results.append({b'id': card[b'id'], 
                       b'name': card[b'name'], 
                       b'board': card.get(b'board', {}).get(b'name', b''), 
                       b'list': card.get(b'list', {}).get(b'name', b''), 
                       b'url': card[b'shortUrl']})

            except Exception as e:
                logger.exception(b'Unexpected error when searching for Trello cards: %s', e)

        return HttpResponse(json.dumps(results), content_type=b'application/json')