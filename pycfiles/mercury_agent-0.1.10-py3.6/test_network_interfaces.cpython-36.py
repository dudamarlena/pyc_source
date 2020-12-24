# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/hwlib/test_network_interfaces.py
# Compiled at: 2018-02-03 12:28:05
# Size of source mod 2**32: 4052 bytes
"""Module to unit test mercury_agent.inspector.hwlib.network_interfaces"""
import mock, pytest, netifaces, mercury_agent.inspector.hwlib.network_interfaces as net_ifs
from tests.unit.base import MercuryAgentUnitTest
FAKE_INTERFACE_LIST = [
 'lo', 'eno1', 'br0', 'virbr0', 'virbr0-nic', 'vnet0']

def fake_ifaddresses_func(interface):
    """Fake netifaces.ifaddresses()."""
    ifaddresses = {'lo':{netifaces.AF_LINK: [{'addr': '93:b9:b7:be:3c:00'}], 
      netifaces.AF_INET: [{'addr': '127.0.0.1'}], 
      netifaces.AF_INET6: [{'addr': '::1'}]}, 
     'eno1':{netifaces.AF_LINK: [{'addr': 'd4:a8:28:a2:19:2f'}], 
      netifaces.AF_INET: [{'addr': '192.168.1.115'}], 
      netifaces.AF_INET6: [{'addr': 'dead:beef::1'}]}, 
     'virbr0':{netifaces.AF_LINK: [{'addr': 'a8:b5:61:1c:de:39'}], 
      netifaces.AF_INET: [{'addr': '192.168.122.1'}], 
      netifaces.AF_INET6: [{'addr': 'dead:beed::1'}]}}
    return ifaddresses.get(interface, {})


class MercuryMiscNetworkInterfacesUnitTests(MercuryAgentUnitTest):
    __doc__ = 'Unit tests for mercury_agent.inspector.hwlib.network_interfaces'

    def setUp(self):
        super(MercuryMiscNetworkInterfacesUnitTests, self).setUp()

    @mock.patch('netifaces.gateways')
    def test_get_default_interface(self, gateways_mock):
        """Tests for get_default_interface()"""
        gateways_mock.return_value = {}
        if not net_ifs.get_default_interface() == '':
            raise AssertionError
        else:
            gateways_mock.return_value = {'default':{2: ('192.168.1.1', 'eth0')}, 
             2:[
              ('192.168.1.1', 'eth0', True)]}
            assert net_ifs.get_default_interface() == 'eth0'

    @mock.patch('netifaces.ifaddresses')
    @mock.patch('netifaces.interfaces')
    def test_get_link_addresses(self, interfaces_mock, ifaddresses_mock):
        """Tests for get_link_addresses()"""
        interfaces_mock.return_value = FAKE_INTERFACE_LIST
        ifaddresses_mock.side_effect = fake_ifaddresses_func
        expected_output = [
         {'interface':'lo', 
          'mac_address':'93:b9:b7:be:3c:00'},
         {'interface':'eno1', 
          'mac_address':'d4:a8:28:a2:19:2f'},
         {'interface':'virbr0', 
          'mac_address':'a8:b5:61:1c:de:39'}]
        assert net_ifs.get_link_addresses(exclude_loopback=False) == expected_output

    @mock.patch('netifaces.ifaddresses')
    @mock.patch('netifaces.interfaces')
    def test_get_ip4_network_info(self, interfaces_mock, ifaddresses_mock):
        """Tests for get_ipv4_network_info()."""
        interfaces_mock.return_value = FAKE_INTERFACE_LIST
        ifaddresses_mock.side_effect = fake_ifaddresses_func
        if not net_ifs.get_ipv4_network_info('not_an_interface') == []:
            raise AssertionError
        elif not net_ifs.get_ipv4_network_info('eno1') == [
         {'addr': '192.168.1.115'}]:
            raise AssertionError

    @mock.patch('netifaces.ifaddresses')
    @mock.patch('netifaces.interfaces')
    def test_get_ip6_network_info(self, interfaces_mock, ifaddresses_mock):
        """Tests for get_ipv6_network_info()."""
        interfaces_mock.return_value = FAKE_INTERFACE_LIST
        ifaddresses_mock.side_effect = fake_ifaddresses_func
        if not net_ifs.get_ipv6_network_info('not_an_interface') == []:
            raise AssertionError
        elif not net_ifs.get_ipv6_network_info('virbr0') == [
         {'addr': 'dead:beed::1'}]:
            raise AssertionError