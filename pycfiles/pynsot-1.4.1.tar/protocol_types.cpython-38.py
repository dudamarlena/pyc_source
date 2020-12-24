# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryanh/src/pynsot/tests/fixtures/protocol_types.py
# Compiled at: 2019-10-24 18:14:13
# Size of source mod 2**32: 1458 bytes
from __future__ import absolute_import, unicode_literals
import pytest
from tests.fixtures import site_client
from six.moves import range

@pytest.fixture
def protocol_type(site_client, protocol_attribute, protocol_attribute2):
    """
    Return a Protocol Type Object.
    """
    return site_client.sites(site_client.default_site).protocol_types.post({'name':'bgp', 
     'required-attributes':[
      'boo', 'foo'], 
     'description':'bgp is my bestie'})


@pytest.fixture
def protocol_attribute(site_client):
    return site_client.sites(site_client.default_site).attributes.post({'name':'boo', 
     'value':'test_attribute', 
     'resource_name':'Protocol'})


@pytest.fixture
def protocol_attribute2(site_client):
    return site_client.sites(site_client.default_site).attributes.post({'name':'foo', 
     'value':'test_attribute', 
     'resource_name':'Protocol'})


@pytest.fixture
def protocol_types(site_client):
    """
    A group of ProtocolTypes for testing limit/offset/etc.
    """
    protocol_types = []
    site = site_client.sites(site_client.default_site)
    for i in range(1, 6):
        protocol_type = site.protocol_types.post({'name': 'type{}'.format(i)})
        protocol_types.append(protocol_type)
    else:
        return protocol_types