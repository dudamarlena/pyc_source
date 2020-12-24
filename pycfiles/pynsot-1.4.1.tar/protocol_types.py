# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryanh/src/pynsot/tests/fixtures/protocol_types.py
# Compiled at: 2019-10-24 21:45:41
from __future__ import absolute_import, unicode_literals
import pytest
from tests.fixtures import site_client
from six.moves import range

@pytest.fixture
def protocol_type(site_client, protocol_attribute, protocol_attribute2):
    """
    Return a Protocol Type Object.
    """
    return site_client.sites(site_client.default_site).protocol_types.post({b'name': b'bgp', 
       b'required-attributes': [
                              b'boo', b'foo'], 
       b'description': b'bgp is my bestie'})


@pytest.fixture
def protocol_attribute(site_client):
    return site_client.sites(site_client.default_site).attributes.post({b'name': b'boo', 
       b'value': b'test_attribute', 
       b'resource_name': b'Protocol'})


@pytest.fixture
def protocol_attribute2(site_client):
    return site_client.sites(site_client.default_site).attributes.post({b'name': b'foo', 
       b'value': b'test_attribute', 
       b'resource_name': b'Protocol'})


@pytest.fixture
def protocol_types(site_client):
    """
    A group of ProtocolTypes for testing limit/offset/etc.
    """
    protocol_types = []
    site = site_client.sites(site_client.default_site)
    for i in range(1, 6):
        protocol_type = site.protocol_types.post({b'name': (b'type{}').format(i)})
        protocol_types.append(protocol_type)

    return protocol_types