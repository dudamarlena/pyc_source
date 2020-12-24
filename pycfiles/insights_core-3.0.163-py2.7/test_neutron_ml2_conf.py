# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_neutron_ml2_conf.py
# Compiled at: 2019-11-14 13:57:46
import doctest
from insights.parsers import neutron_ml2_conf
from insights.parsers.neutron_ml2_conf import NeutronMl2Conf
from insights.tests import context_wrap
neutron_ml2_content = '\n[DEFAULT]\nverbose=True\ndebug=False\n[ml2]\ntype_drivers=vxlan,vlan,flat,gre\ntenant_network_types=vxlan\nmechanism_drivers=openvswitch\nextension_drivers=qos,port_security\npath_mtu=0\noverlay_ip_version=4\n[ml2_type_flat]\nflat_networks=datacentre\n[ml2_type_geneve]\n[ml2_type_gre]\ntunnel_id_ranges=1:4094\n[ml2_type_vlan]\nnetwork_vlan_ranges=datacentre:1:1000\n[ml2_type_vxlan]\nvni_ranges=1:4094\nvxlan_group=224.0.0.1\n[securitygroup]\nfirewall_driver=iptables_hybrid\n'

def test_neutron_ml2_conf():
    result = NeutronMl2Conf(context_wrap(neutron_ml2_content))
    assert result.get('ml2_type_flat', 'flat_networks') == 'datacentre'
    assert result.get('ml2', 'tenant_network_types') == 'vxlan'
    assert result.get('ml2', 'mechanism_drivers') == 'openvswitch'
    assert result.get('securitygroup', 'firewall_driver') == 'iptables_hybrid'


def test_neutron_ml2_conf_docs():
    failed, total = doctest.testmod(neutron_ml2_conf, globs={'neutron_ml2_conf': NeutronMl2Conf(context_wrap(neutron_ml2_content))})
    assert failed == 0