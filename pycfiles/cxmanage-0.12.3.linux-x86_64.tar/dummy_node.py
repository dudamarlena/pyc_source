# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/tests/dummy_node.py
# Compiled at: 2017-02-08 04:42:30
""" Dummy implementation for cxmanage_api.node.Node """
import random
from cxmanage_api.ubootenv import UbootEnv
from cxmanage_api.tests import Dummy, DummyBMC, TestSensor
from cxmanage_api.node import Node

class DummyNode(Dummy):
    """ Dummy node """
    dummy_spec = Node
    ip_addresses = DummyBMC.ip_addresses

    def __init__(self, ip_address, username='admin', password='admin', tftp=None, *args, **kwargs):
        super(DummyNode, self).__init__()
        self.power_state = False
        self.ip_address = ip_address
        self.tftp = tftp
        self.sel = []
        self.bmc = DummyBMC()
        self._chassis_id = 0

    @property
    def guid(self):
        """Returns the node GUID"""
        return self.bmc.unique_guid

    @property
    def chassis_id(self):
        """Returns the chasis ID."""
        return self._chassis_id

    def get_sel(self):
        """Simulate get_sel()"""
        return self.sel

    def get_power(self):
        """Simulate get_power(). """
        return self.power_state

    def get_power_policy(self):
        """Simulate get_power_policy(). """
        return 'always-off'

    def get_sensors(self, name=''):
        """Simulate get_sensors(). """
        power_value = '%f (+/- 0) Watts' % random.uniform(0, 10)
        temp_value = '%f (+/- 0) degrees C' % random.uniform(30, 50)
        sensors = [
         TestSensor('Node Power', power_value),
         TestSensor('Board Temp', temp_value)]
        return [ s for s in sensors if name.lower() in s.sensor_name.lower() ]

    def get_boot_order(self):
        """Simulate get_boot_order(). """
        return [
         'disk', 'pxe']

    def get_pxe_interface(self):
        """Simulate get_pxe_interface(). """
        return 'eth0'

    def get_versions(self):
        """Simulate get_versions(). """

        class Result(object):
            """Result Class. """

            def __init__(self):
                self.header = 'Calxeda SoC (0x0096CD)'
                self.hardware_version = 'TestBoard X00'
                self.firmware_version = 'v0.0.0'
                self.ecme_version = 'v0.0.0'
                self.ecme_timestamp = '0'
                self.a9boot_version = 'v0.0.0'
                self.uboot_version = 'v0.0.0'
                self.chip_name = 'Unknown'

        return Result()

    def ipmitool_command(self, ipmitool_args):
        """Simulate ipmitool_command(). """
        return 'Dummy output'

    def get_ubootenv(self):
        """Simulate get_ubootenv(). """
        ubootenv = UbootEnv()
        ubootenv.variables['bootcmd0'] = 'run bootcmd_default'
        ubootenv.variables['bootcmd_default'] = 'run bootcmd_sata'
        return ubootenv

    @staticmethod
    def get_fabric_ipinfo():
        """Simulates get_fabric_ipinfo(). """
        return {}

    def get_server_ip(self, interface=None, ipv6=False, aggressive=False):
        """Simulate get_server_ip(). """
        return '192.168.200.1'

    def get_fabric_macaddrs(self):
        """Simulate get_fabric_macaddrs(). """
        result = {}
        for node in range(len(self.ip_addresses)):
            result[node] = {}
            for port in range(3):
                address = '00:00:00:00:%02x:%02x' % (node, port)
                result[node][port] = address

        return result

    def get_fabric_uplink_info(self):
        """Simulate get_fabric_uplink_info(). """
        results = {}
        for nid in range(1, len(self.ip_addresses)):
            results[nid] = {'eth0': 0, 'eth1': 0, 'mgmt': 0}

        return results

    def get_uplink_info(self):
        """Simulate get_uplink_info(). """
        return 'Node 0: eth0 0, eth1 0, mgmt 0'

    def get_uplink_speed(self):
        """Simulate get_uplink_speed(). """
        return 1

    def get_link_stats(self, link=0):
        """Simulate get_link_stats(). """
        return {'FS_LC%s_BYTE_CNT_0' % link: '0x0', 
           'FS_LC%s_BYTE_CNT_1' % link: '0x0', 
           'FS_LC%s_CFG_0' % link: '0x1030107f', 
           'FS_LC%s_CFG_1' % link: '0x104f', 
           'FS_LC%s_CM_RXDATA_0' % link: '0x0', 
           'FS_LC%s_CM_RXDATA_1' % link: '0x0', 
           'FS_LC%s_CM_TXDATA_0' % link: '0x0', 
           'FS_LC%s_CM_TXDATA_1' % link: '0x0', 
           'FS_LC%s_PKT_CNT_0' % link: '0x0', 
           'FS_LC%s_PKT_CNT_1' % link: '0x0', 
           'FS_LC%s_RDRPSCNT' % link: '0x0', 
           'FS_LC%s_RERRSCNT' % link: '0x0', 
           'FS_LC%sRMCSCNT' % link: '0x0', 
           'FS_LC%s_RPKTSCNT' % link: '0x0', 
           'FS_LC%s_RUCSCNT' % link: '0x0', 
           'FS_LC%s_SC_STAT' % link: '0x0', 
           'FS_LC%s_STATE' % link: '0x1033', 
           'FS_LC%s_TDRPSCNT' % link: '0x0', 
           'FS_LC%s_TPKTSCNT' % link: '0x1'}

    def get_linkmap(self):
        """Simulate get_linkmap(). """
        results = {}
        for nid in range(0, len(self.ip_addresses)):
            results[nid] = {nid: {1: 2, 3: 1, 4: 3}}

        return results

    def get_routing_table(self):
        """Simulate get_routing_table(). """
        results = {}
        for nid in range(0, len(self.ip_addresses)):
            results[nid] = {nid: {1: [0, 0, 0, 3, 0], 2: [
                       0, 3, 0, 0, 2], 
                     3: [
                       0, 2, 0, 0, 3]}}

        return results

    def get_depth_chart(self):
        """Simulate get_depth_chart(). """
        results = {}
        for nid in range(0, len(self.ip_addresses)):
            results[nid] = {nid: {1: {'shortest': (0, 0)}, 2: {'hops': [(3, 1)], 'shortest': (0, 0)}, 3: {'hops': [(2, 1)], 'shortest': (0, 0)}}}

        return results

    def get_uplink(self, iface):
        """Simulate get_uplink(). """
        return 0

    def get_node_fru_version(self):
        """Simulate get_node_fru_version(). """
        return '0.0'

    def get_slot_fru_version(self):
        """Simulate get_slot_fru_version(). """
        return '0.0'


class DummyFailNode(DummyNode):
    """ Dummy node that should fail on some commands """

    class DummyFailError(Exception):
        """Dummy Fail Error class."""
        pass

    def get_power(self):
        """Simulate get_power(). """
        raise DummyFailNode.DummyFailError