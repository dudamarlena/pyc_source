# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/ticketbis/tests/test_events.py
# Compiled at: 2019-05-02 11:49:29
import logging
log = logging.getLogger(__name__)
import os
from . import TEST_DATA_DIR, BaseAuthenticatedEndpointTestCase

class EventsEndpointTestCase(BaseAuthenticatedEndpointTestCase):
    """
    General
    """

    def test_events(self):
        response = self.api.events(params={'max': 2, 'offset': 0})
        assert 'id' in response[0]
        assert self.api.page_max == 2
        assert self.api.page_offset == 0
        response = self.api.events(response[0]['id'])
        assert 'name' in response

    def test_events_by_category(self):
        response = self.api.categories.events(self.default_category_id, params={'max': 2, 'offset': 0})
        assert 'name' in response[0]

    def test_event_pagination(self):
        response = self.api.events(auto_pagination=True, params={'max': 1})
        r = next(response)
        r = next(response)
        assert 'name' in r