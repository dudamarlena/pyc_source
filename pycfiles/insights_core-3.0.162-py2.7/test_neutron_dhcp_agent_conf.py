# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_neutron_dhcp_agent_conf.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import neutron_dhcp_agent_conf
from insights.parsers.neutron_dhcp_agent_conf import NeutronDhcpAgentIni
from insights.tests import context_wrap
DHCP_AGENT_INI = ('\n[DEFAULT]\n\novs_integration_bridge = br-int\novs_use_veth = false\ninterface_driver = neutron.agent.linux.interface.OVSInterfaceDriver\novs_vsctl_timeout = 10\nresync_interval = 30\ndhcp_driver = neutron.agent.linux.dhcp.Dnsmasq\nenable_isolated_metadata = True\nforce_metadata = True\nenable_metadata_network = False\nroot_helper=sudo neutron-rootwrap /etc/neutron/rootwrap.conf\nstate_path=/var/lib/neutron\n\n[AGENT]\n\nreport_interval = 30\nlog_agent_heartbeats = false\navailability_zone = nova\n').strip()

def test_neutron_dhcp_agent_ini():
    data = NeutronDhcpAgentIni(context_wrap(DHCP_AGENT_INI))
    assert data.has_option('AGENT', 'log_agent_heartbeats')
    assert data.get('DEFAULT', 'force_metadata') == 'True'
    assert data.getint('DEFAULT', 'ovs_vsctl_timeout') == 10


def test_neutron_dhcp_agent_ini_doc():
    env = {'data': NeutronDhcpAgentIni(context_wrap(DHCP_AGENT_INI))}
    failed, total = doctest.testmod(neutron_dhcp_agent_conf, globs=env)
    assert failed == 0