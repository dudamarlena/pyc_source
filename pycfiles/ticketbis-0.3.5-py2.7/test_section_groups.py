# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/ticketbis/tests/test_section_groups.py
# Compiled at: 2019-05-02 11:49:29
import logging
log = logging.getLogger(__name__)
import os
from . import TEST_DATA_DIR, BaseAuthenticatedEndpointTestCase

class SectionGroupsEndpointTestCase(BaseAuthenticatedEndpointTestCase):
    """
    General
    """

    def test_section_groups_by_event(self):
        response = self.api.events(params={'max': 1, 'offset': 0})
        assert 'id' in response[0]
        response = self.api.events.section_groups(response[0]['id'])
        assert 'name' in response[0]