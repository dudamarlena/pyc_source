# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ryanh/src/pynsot/tests/fixtures/protocols.py
# Compiled at: 2019-10-24 21:45:41
from __future__ import absolute_import, unicode_literals
import pytest
from tests.fixtures import protocol_type, site_client
from .circuits import circuit, device_a, interface_a
from six.moves import range

@pytest.fixture
def protocol(site_client, device_a, interface_a, circuit, protocol_type):
    """
    Return a Protocol Object.
    """
    device_id = device_a[b'id']
    interface_slug = interface_a[b'name_slug']
    return site_client.sites(site_client.default_site).protocols.post({b'device': device_id, 
       b'type': b'bgp', 
       b'interface': interface_slug, 
       b'attributes': {b'foo': b'test_protocol'}, b'circuit': circuit[b'name'], 
       b'description': b'bgp is the best'})


@pytest.fixture
def protocol_attribute(site_client):
    return site_client.sites(site_client.default_site).attributes.post({b'name': b'boo', 
       b'value': b'test_attribute', 
       b'resource_name': b'Protocol'})


@pytest.fixture
def protocol_attribute2(site_client):
    return site_client.sites(site_client.default_site).attributes.post({b'name': b'foo', 
       b'value': b'test_protocol', 
       b'resource_name': b'Protocol'})


@pytest.fixture
def protocols(site_client, protocol_type, protocol_attribute2):
    """
    A group of Protocol objects for testing limit/offest/etc.
    """
    protocols = []
    site = site_client.sites(site_client.default_site)
    for i in range(1, 6):
        device_name = (b'device{:02d}').format(i)
        interface_name = (b'Ethernet1/{}').format(i)
        device = site.devices.post({b'hostname': device_name})
        interface = site.interfaces.post({b'device': device[b'id'], 
           b'name': interface_name})
        protocol = site.protocols.post({b'type': protocol_type[b'name'], 
           b'device': device[b'id'], 
           b'interface': interface[b'id'], 
           b'attributes': {b'foo': b'bar'}})
        protocols.append(protocol)

    return protocols