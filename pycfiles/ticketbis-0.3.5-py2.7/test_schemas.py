# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/ticketbis/tests/test_schemas.py
# Compiled at: 2019-05-02 11:49:29
import logging
log = logging.getLogger(__name__)
import os
from . import TEST_DATA_DIR, BaseAuthenticatedEndpointTestCase

class SchemasEndpointTestCase(BaseAuthenticatedEndpointTestCase):
    """
    General
    """

    def test_schema(self):
        response = self.api.schemas(self.default_schema_id)
        assert 'name' in response

    def test_schemas(self):
        response = self.api.schemas(params={'max': 2, 'offset': 0})
        assert 'name' in response[0]
        assert self.api.page_max == 2
        assert self.api.page_offset == 0

    def test_schemas_by_venue(self):
        response = self.api.venues.schemas(self.default_venue_id)
        assert 'name' in response[0]