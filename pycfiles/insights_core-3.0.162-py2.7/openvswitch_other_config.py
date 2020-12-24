# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/openvswitch_other_config.py
# Compiled at: 2019-05-16 13:41:33
"""
OpenvSwitchOtherConfig - command ``ovs-vsctl -t 5 get Open_vSwitch . other_config``
===================================================================================

Class OpenvSwitchOtherConfig process the output of the following OpenvSwitch command:

ovs-vsctl -t 5 get Open_vSwitch . other_config

Sample input::

    {dpdk-init="true", dpdk-lcore-mask="30000003000", dpdk-socket-mem="4096,4096", pmd-cpu-mask="30000003000"}

Examples:

    >>> type(ovs_other_conf)
    <class 'insights.parsers.openvswitch_other_config.OpenvSwitchOtherConfig'>
    >>> ovs_other_conf.get("dpdk-init")
    true
    >>> ovs_other_conf["dpdk-lcore-mask"]
    30000003000
    >>> dpdk-socket-mem in ovs_other_conf
    True

"""
from .. import parser, LegacyItemAccess, CommandParser
from insights.specs import Specs
from . import optlist_to_dict

@parser(Specs.openvswitch_other_config)
class OpenvSwitchOtherConfig(LegacyItemAccess, CommandParser):
    """Parses output of the ovs-vsctl -t 5 get Open_vSwitch . other_config command"""

    def parse_content(self, content):
        self.data = {}
        one_line_content = ('').join(content).strip()
        if one_line_content.startswith('{'):
            new_line = one_line_content.strip('{}')
            if new_line:
                self.data = optlist_to_dict(new_line, opt_sep=', ', strip_quotes=True)