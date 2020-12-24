# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryanh/src/pynsot/tests/test_client.py
# Compiled at: 2019-10-16 17:52:59
# Size of source mod 2**32: 797 bytes
__doc__ = '\nTest the API client.\n'
from __future__ import unicode_literals
import logging, pytest
from pynsot.util import get_result
from .fixtures import config, client
__all__ = ('client', 'config', 'pytest')
log = logging.getLogger(__name__)

def test_authentication(client):
    """Test manual client authentication."""
    auth = {'email':client.config['email'], 
     'secret_key':client.config['secret_key']}
    resp = client.authenticate.post(auth)
    result = get_result(resp)
    assert 'auth_token' in result


def test_sites(client):
    """Test working with sites using the client."""
    site = client.sites.post({'name': 'Foo'})
    assert client.sites.get() == [site]
    assert client.sites(site['id']).get() == site