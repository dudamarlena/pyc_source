# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_neutron_l3_agent_conf.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import neutron_l3_agent_conf
from insights.parsers.neutron_l3_agent_conf import NeutronL3AgentIni
from insights.tests import context_wrap
L3_AGENT_INI = ("\n[DEFAULT]\n\n#\n# From neutron.base.agent\n#\n\n# Name of Open vSwitch bridge to use (string value)\novs_integration_bridge = br-int\n\n# Uses veth for an OVS interface or not. Support kernels with limited namespace\n# support (e.g. RHEL 6.5) so long as ovs_use_veth is set to True. (boolean\n# value)\novs_use_veth = false\n\n# The driver used to manage the virtual interface. (string value)\n#interface_driver = <None>\ninterface_driver = neutron.agent.linux.interface.OVSInterfaceDriver\n\n# Timeout in seconds for ovs-vsctl commands. If the timeout expires, ovs\n# commands will fail with ALARMCLOCK error. (integer value)\novs_vsctl_timeout = 10\n\n#\n# From neutron.l3.agent\n#\n\n# The working mode for the agent. Allowed modes are: 'legacy' - this preserves\n# the existing behavior where the L3 agent is deployed on a centralized\n# networking node to provide L3 services like DNAT, and SNAT. Use this mode if\n# you do not want to adopt DVR. 'dvr' - this mode enables DVR functionality and\n# must be used for an L3 agent that runs on a compute host. 'dvr_snat' - this\n# enables centralized SNAT support in conjunction with DVR.  This mode must be\n# used for an L3 agent running on a centralized node (or in single-host\n# deployments, e.g. devstack) (string value)\n# Allowed values: dvr, dvr_snat, legacy\nagent_mode = dvr\n\n# TCP Port used by Neutron metadata namespace proxy. (port value)\n# Minimum value: 0\n# Maximum value: 65535\nmetadata_port = 9697\n\n# Send this many gratuitous ARPs for HA setup, if less than or equal to 0, the\n# feature is disabled (integer value)\n#send_arp_for_ha = 3\n\n# Allow running metadata proxy. (boolean value)\nenable_metadata_proxy = true\n\n# DEPRECATED: Name of bridge used for external network traffic. When this\n# parameter is set, the L3 agent will plug an interface directly into an\n# external bridge which will not allow any wiring by the L2 agent. Using this\n# will result in incorrect port statuses. This option is deprecated and will be\n# removed in Ocata. (string value)\n# This option is deprecated for removal.\n# Its value may be silently ignored in the future.\nexternal_network_bridge =\n\n#\n# From oslo.log\n#\n\n# If set to true, the logging level will be set to DEBUG instead of the default\n# INFO level. (boolean value)\n# Note: This option can be changed without restarting.\ndebug = False\n\n# Defines the format string for %%(asctime)s in log records. Default:\n# %(default)s . This option is ignored if log_config_append is set. (string\n# value)\nlog_date_format = %Y-%m-%d %H:%M:%S\n\n[AGENT]\n\n#\n# From neutron.base.agent\n#\n\n# Seconds between nodes reporting state to server; should be less than\n# agent_down_time, best if it is half or less than agent_down_time. (floating\n# point value)\nreport_interval = 30\n\n# Log agent heartbeats (boolean value)\nlog_agent_heartbeats = false\n\n# Availability zone of this node (string value)\navailability_zone = nova\n").strip()

def test_neutron_l3_agent_ini():
    nla_ini = NeutronL3AgentIni(context_wrap(L3_AGENT_INI))
    assert nla_ini.has_option('AGENT', 'log_agent_heartbeats')
    assert nla_ini.get('DEFAULT', 'agent_mode') == 'dvr'
    assert nla_ini.getint('DEFAULT', 'metadata_port') == 9697


def test_doc():
    env = {'l3_agent_ini': NeutronL3AgentIni(context_wrap(L3_AGENT_INI, path='/etc/neutron/l3_agent.ini'))}
    failed, total = doctest.testmod(neutron_l3_agent_conf, globs=env)
    assert failed == 0