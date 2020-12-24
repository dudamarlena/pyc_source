# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/ticketbis/tests/test_oauth.py
# Compiled at: 2019-05-02 11:49:29
import logging
log = logging.getLogger(__name__)
from . import BaseAuthenticationTestCase
import six, ticketbis

class OAuthEndpointTestCase(BaseAuthenticationTestCase):

    def test_auth_url(self):
        url = self.api.oauth.auth_url()
        assert isinstance(url, six.string_types)

    def test_get_token(self):
        pass