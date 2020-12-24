# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryanh/src/pynsot/tests/fixtures/circuits.py
# Compiled at: 2019-10-24 21:45:41
from __future__ import absolute_import, unicode_literals
import pytest
from tests.fixtures import site_client
from six.moves import map

@pytest.fixture
def circuit_attributes(site_client):
    attr_names = [
     b'owner',
     b'vendor']
    attrs = ({b'name': a, b'resource_name': b'Circuit'} for a in attr_names)
    client = site_client.sites(site_client.default_site).attributes
    return list(map(client.post, attrs))


@pytest.fixture
def device_a(site_client):
    """ Device for the A side of the circuit """
    return site_client.sites(site_client.default_site).devices.post({b'hostname': b'foo-bar01'})


@pytest.fixture
def device_z(site_client):
    """ Device for the Z side of the circuit """
    return site_client.sites(site_client.default_site).devices.post({b'hostname': b'foo-bar02'})


@pytest.fixture
def interface_a(site_client, device_a, network):
    """ Interface for the A side of the circuit """
    return site_client.sites(site_client.default_site).interfaces.post({b'device': device_a[b'id'], 
       b'name': b'eth0', 
       b'addresses': [
                    b'10.20.30.2/32']})


@pytest.fixture
def interface_z(site_client, device_z, network):
    """ Interface for the Z side of the circuit """
    return site_client.sites(site_client.default_site).interfaces.post({b'device': device_z[b'id'], 
       b'name': b'eth0', 
       b'addresses': [
                    b'10.20.30.3/32']})


@pytest.fixture
def circuit(site_client, circuit_attributes, interface_a, interface_z):
    """ Circuit connecting interface_a to interface_z """
    return site_client.sites(site_client.default_site).circuits.post({b'name': b'test_circuit', 
       b'endpoint_a': interface_a[b'id'], 
       b'endpoint_z': interface_z[b'id'], 
       b'attributes': {b'owner': b'alice', 
                       b'vendor': b'lasers go pew pew'}})


@pytest.fixture
def dangling_circuit(site_client, interface):
    """
    Circuit where we only own the local site, remote (Z) end is a vendor
    """
    return site_client.sites(site_client.default_site).circuits.post({b'name': b'remote_vendor_circuit', 
       b'endpoint_a': interface[b'id']})


@pytest.fixture
def attributeless_circuit(site_client, interface):
    """ Circuit with no attributes set """
    return site_client.sites(site_client.default_site).circuits.post({b'name': b'attributeless_circuit', 
       b'endpoint_a': interface[b'id'], 
       b'attributes': {}})