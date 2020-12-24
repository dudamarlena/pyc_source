# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbintegrations/trello/tests.py
# Compiled at: 2020-01-07 04:31:42
"""Unit tests for the Trello integration."""
from __future__ import unicode_literals
from django.http import HttpResponse
from reviewboard.site.urlresolvers import local_site_reverse
from rbintegrations.testing.testcases import IntegrationTestCase
from rbintegrations.trello.integration import TrelloIntegration
from rbintegrations.trello.views import TrelloCardSearchView

class TrelloIntegrationTests(IntegrationTestCase):
    """Tests for Trello."""
    integration_cls = TrelloIntegration
    fixtures = [b'test_site', b'test_users']

    def test_card_search(self):
        """Testing TrelloCardSearchView"""
        self.spy_on(TrelloCardSearchView.get, call_fake=lambda self, request, **kwargs: HttpResponse(b'{}', content_type=b'application/json'))
        review_request = self.create_review_request(public=True)
        rsp = self.client.get(local_site_reverse(b'trello-card-search', kwargs={b'review_request_id': review_request.display_id}))
        self.assertEqual(rsp.status_code, 200)

    def test_card_search_unpublished(self):
        """Testing TrelloCardSearchView with an unpublished review request"""
        self.spy_on(TrelloCardSearchView.get, call_fake=lambda self, request, **kwargs: HttpResponse(b'{}', content_type=b'application/json'))
        review_request = self.create_review_request(public=False)
        rsp = self.client.get(local_site_reverse(b'trello-card-search', kwargs={b'review_request_id': review_request.display_id}))
        self.assertEqual(rsp.status_code, 403)

    def test_card_search_with_local_site(self):
        """Testing TrelloCardSearchView with a Local Site"""
        self.spy_on(TrelloCardSearchView.get, call_fake=lambda self, request, **kwargs: HttpResponse(b'{}', content_type=b'application/json'))
        self.client.login(username=b'doc', password=b'doc')
        review_request = self.create_review_request(public=True, with_local_site=True)
        rsp = self.client.get(local_site_reverse(b'trello-card-search', local_site_name=review_request.local_site.name, kwargs={b'review_request_id': review_request.display_id}))
        self.assertEqual(rsp.status_code, 200)

    def test_card_search_with_local_site_no_access(self):
        """Testing TrelloCardSearchView with a Local Site that the user does
        not have access to
        """
        self.spy_on(TrelloCardSearchView.get, call_fake=lambda self, request, **kwargs: HttpResponse(b'{}', content_type=b'application/json'))
        self.client.login(username=b'dopey', password=b'dopey')
        review_request = self.create_review_request(public=True, with_local_site=True)
        rsp = self.client.get(local_site_reverse(b'trello-card-search', local_site_name=review_request.local_site.name, kwargs={b'review_request_id': review_request.display_id}))
        self.assertEqual(rsp.status_code, 403)