# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_bond.py
# Compiled at: 2020-04-16 14:56:28
import doctest, pytest
from insights.parsers import ParseException
from insights.parsers.bond import Bond
from insights.parsers import bond
from insights.tests import context_wrap
CONTEXT_PATH = 'proc/net/bonding/bond0'
BONDINFO_1 = ('\nEthernet Channel Bonding Driver: v3.7.1 (April 27, 2011)\n\nBonding Mode: load balancing (round-robin)\nMII Status: up\nMII Polling Interval (ms): 100\nUp Delay (ms): 0\nDown Delay (ms): 0\n\nSlave Interface: eno1\nMII Status: up\nSpeed: 1000 Mbps\nDuplex: full\nLink Failure Count: 0\nPermanent HW addr: 2c:44:fd:80:5c:f8\nSlave queue ID: 0\n\nSlave Interface: eno2\nMII Status: up\nSpeed: 1000 Mbps\nDuplex: full\nLink Failure Count: 0\nPermanent HW addr: 2c:44:fd:80:5c:f9\nSlave queue ID: 0\n').strip()
BONDINFO_MODE_4 = ('\nEthernet Channel Bonding Driver: v3.2.4 (January 28, 2008)\n\nBonding Mode: IEEE 802.3ad Dynamic link aggregation\nTransmit Hash Policy: layer2 (0)\nMII Status: up\nMII Polling Interval (ms): 500\nUp Delay (ms): 0\nDown Delay (ms): 0\n\n802.3ad info\nLACP rate: slow\nActive Aggregator Info:\n        Aggregator ID: 3\n        Number of ports: 1\n        Actor Key: 17\n        Partner Key: 1\n        Partner Mac Address: 00:00:00:00:00:00\n\nSlave Interface: eth1\nMII Status: up\nSpeed: 1000 Mbps\nDuplex: full\nLink Failure Count: 0\nPermanent HW addr: 00:16:35:5e:42:fc\nAggregator ID: 3\n\nSlave Interface: eth2\nMII Status: up\nSpeed: 1000 Mbps\nDuplex: full\nSpeed\nLink Failure Count: 0\nPermanent HW addr: 00:16:35:5e:02:7e\nAggregator ID: 2\n').strip()
BONDINFO_MODE_2 = ('\nEthernet Channel Bonding Driver: v3.7.1 (April 27, 2011)\n\nBonding Mode: load balancing (xor)\nTransmit Hash Policy: layer2+3 (2)\nMII Status: up\nMII Polling Interval (ms): 100\nUp Delay (ms): 0\nDown Delay (ms): 0\n\nSlave Interface: eno1\nMII Status: up\nSpeed: 1000 Mbps\nDuplex: full\nLink Failure Count: 0\nPermanent HW addr: 2c:44:fd:80:5c:f8\nSlave queue ID: 0\n\nSlave Interface: eno2\nMII Status: up\nSpeed: 1000 Mbps\nDuplex: full\nLink Failure Count: 0\nPermanent HW addr: 2c:44:fd:80:5c:f9\nSlave queue ID: 0\n').strip()
BONDINFO_CORRUPT = ('\nLink Failure Count: 0\nPermanent HW addr: 00:16:35:5e:02:7e\nAggregator ID:\n').strip()
BONDINFO_UNKNOWN_BOND_MODE = ('\nBonding Mode: reverse proximity hash combination mode\n').strip()
BONDINFO_MODE_5 = ('\nEthernet Channel Bonding Driver: v3.7.1 (April 27, 2011)\n\nBonding Mode: fault-tolerance (active-backup)\nPrimary Slave: None\nCurrently Active Slave: enp17s0f0\nMII Status: up\nMII Polling Interval (ms): 100\nUp Delay (ms): 0\nDown Delay (ms): 0\n\nSlave Interface: enp17s0f0\nMII Status: up\nSpeed: 10000 Mbps\nDuplex: full\nLink Failure Count: 0\nPermanent HW addr: 00:1f:f3:af:d3:f0\nSlave queue ID: 0\n\nSlave Interface: enp17s0f1\nMII Status: up\nSpeed: 10000 Mbps\nDuplex: full\nLink Failure Count: 0\nPermanent HW addr: 00:1f:f3:af:d3:f1\nSlave queue ID: 0\n').strip()
BONDINFO_MODE_6 = BONDINFO_MODE_5.replace('Currently Active Slave: enp17s0f0', '')
BONDINFO_MODE_7 = ('\nEthernet Channel Bonding Driver: v3.7.1 (April 27, 2011)\n\nBonding Mode: fault-tolerance (active-backup)\nPrimary Slave: em3 (primary_reselect failure)\nCurrently Active Slave: em3\nMII Status: up\nMII Polling Interval (ms): 0\nUp Delay (ms): 0\nDown Delay (ms): 0\nARP Polling Interval (ms): 1000\nARP IP target/s (n.n.n.n form): 10.152.1.1\n\nSlave Interface: em3\nMII Status: up\nSpeed: 1000 Mbps\nDuplex: full\nLink Failure Count: 92028\nPermanent HW addr: 00:1f:f3:af:d3:f1\nSlave queue ID: 0\n\nSlave Interface: p2p3\nMII Status: up\nSpeed: 1000 Mbps\nDuplex: full\nLink Failure Count: 71524\nPermanent HW addr: 00:1f:f3:af:d3:f1\nSlave queue ID: 0\n').strip()
BOND_MODE_4 = ('\nEthernet Channel Bonding Driver: v3.7.1 (April 27, 2011)\n\nBonding Mode: IEEE 802.3ad Dynamic link aggregation\nTransmit Hash Policy: layer2 (0)\nMII Status: up\nMII Polling Interval (ms): 100\nUp Delay (ms): 2000\nDown Delay (ms): 1000\n\n802.3ad info\nLACP rate: slow\nMin links: 0\nAggregator selection policy (ad_select): stable\nSystem priority: 65535\nSystem MAC address: 08:00:27:99:a3:6b\nActive Aggregator Info:\n\t\t\t\tAggregator ID: 1\n\t\t\t\tNumber of ports: 1\n\t\t\t\tActor Key: 9\n\t\t\t\tPartner Key: 1\n\t\t\t\tPartner Mac Address: 00:00:00:00:00:00\n\nSlave Interface: enp0s9\nMII Status: up\nSpeed: 1000 Mbps\nDuplex: full\nLink Failure Count: 0\nPermanent HW addr: 08:00:27:99:a3:6b\nSlave queue ID: 0\nAggregator ID: 1\nActor Churn State: none\nPartner Churn State: churned\nActor Churned Count: 0\nPartner Churned Count: 1\ndetails actor lacp pdu:\n    system priority: 65535\n    system mac address: 08:00:27:99:a3:6b\n    port key: 9\n    port priority: 255\n    port number: 1\n    port state: 77\ndetails partner lacp pdu:\n    system priority: 65535\n    system mac address: 00:00:00:00:00:00\n    oper key: 1\n    port priority: 255\n    port number: 1\n    port state: 1\n\nSlave Interface: enp0s8\nMII Status: down\nSpeed: Unknown\nDuplex: Unknown\nLink Failure Count: 0\nPermanent HW addr: 08:00:27:a2:8d:f5\nSlave queue ID: 0\nAggregator ID: 2\nActor Churn State: churned\nPartner Churn State: churned\nActor Churned Count: 1\nPartner Churned Count: 1\ndetails actor lacp pdu:\n    system priority: 65535\n    system mac address: 08:00:27:99:a3:6b\n    port key: 0\n    port priority: 255\n    port number: 2\n    port state: 69\ndetails partner lacp pdu:\n    system priority: 65535\n    system mac address: 00:00:00:00:00:00\n    oper key: 1\n    port priority: 255\n    port number: 1\n    port state: 1\n').strip()

def test_netstat_doc_examples():
    env = {'bond_info': Bond(context_wrap(BONDINFO_MODE_4))}
    failed, total = doctest.testmod(bond, globs=env)
    assert failed == 0


def test_bond_class():
    bond_obj = Bond(context_wrap(BONDINFO_1, CONTEXT_PATH))
    assert bond_obj.file_name == 'bond0'
    assert not bond_obj.partner_mac_address
    assert bond_obj.bond_mode == '0'
    assert bond_obj.slave_interface == ['eno1', 'eno2']
    assert bond_obj.up_delay == '0'
    assert bond_obj.down_delay == '0'
    assert bond_obj.data['eno1']['speed'] == '1000 Mbps'
    assert bond_obj.data['eno1']['mii_status'] == 'up'
    assert bond_obj.data['eno2']['mii_status'] == 'up'
    bond_obj = Bond(context_wrap(BONDINFO_MODE_4, CONTEXT_PATH))
    assert bond_obj.bond_mode == '4'
    assert bond_obj.partner_mac_address == '00:00:00:00:00:00'
    assert bond_obj.aggregator_id == ['3', '3', '2']
    assert bond_obj.xmit_hash_policy == 'layer2'
    assert bond_obj.active_slave is None
    bond_obj = Bond(context_wrap(BONDINFO_CORRUPT, CONTEXT_PATH))
    assert bond_obj.bond_mode is None
    assert bond_obj.slave_interface == []
    assert not bond_obj.xmit_hash_policy
    bond_obj = Bond(context_wrap(BONDINFO_MODE_2, CONTEXT_PATH))
    assert bond_obj.xmit_hash_policy == 'layer2+3'
    bond_obj = Bond(context_wrap(BONDINFO_MODE_5, CONTEXT_PATH))
    assert bond_obj.bond_mode == '1'
    assert bond_obj.active_slave == 'enp17s0f0'
    bond_obj_2 = Bond(context_wrap(BONDINFO_MODE_6, CONTEXT_PATH))
    assert bond_obj_2.bond_mode == '1'
    assert bond_obj_2.active_slave is None
    bond_obj_3 = Bond(context_wrap(BONDINFO_1, CONTEXT_PATH))
    assert bond_obj_3.file_name == 'bond0'
    assert bond_obj_3.slave_interface == ['eno1', 'eno2']
    assert bond_obj_3.slave_duplex == ['full', 'full']
    assert bond_obj_3.slave_speed == ['1000 Mbps', '1000 Mbps']
    assert bond_obj_3.slave_link_failure_count == ['0', '0']
    assert bond_obj_3.mii_status == ['up', 'up', 'up']
    assert bond_obj_3.arp_polling_interval is None
    assert bond_obj_3.arp_ip_target is None
    bond_obj_4 = Bond(context_wrap(BONDINFO_MODE_7, CONTEXT_PATH))
    assert bond_obj_4.file_name == 'bond0'
    assert bond_obj_4.arp_polling_interval == '1000'
    assert bond_obj_4.arp_ip_target == '10.152.1.1'
    assert bond_obj_4.primary_slave == 'em3 (primary_reselect failure)'
    bond_obj = Bond(context_wrap(BOND_MODE_4, CONTEXT_PATH))
    assert bond_obj.file_name == 'bond0'
    assert bond_obj.up_delay == '2000'
    assert bond_obj.down_delay == '1000'
    assert bond_obj.data['mii_status'] == 'up'
    assert bond_obj.data['enp0s9']['mii_status'] == 'up'
    assert bond_obj.data['enp0s8']['mii_status'] == 'down'
    assert bond_obj.data['enp0s8']['aggregator_id'] == '2'
    assert bond_obj.data['enp0s9']['aggregator_id'] == '1'
    with pytest.raises(ParseException) as (exc):
        bond_obj = Bond(context_wrap(BONDINFO_UNKNOWN_BOND_MODE, CONTEXT_PATH))
        assert not bond_obj.bond_mode
    assert 'Unrecognised bonding mode' in str(exc)
    return