# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/ovs_vsctl_list_bridge.py
# Compiled at: 2019-05-16 13:41:33
"""
OVSvsctlListBridge - command ``/usr/bin/ovs-vsctl list bridge``
===============================================================

This module provides class ``OVSvsctlListBridge`` for parsing the
output of command ``ovs-vsctl list bridge``.
"""
from insights import CommandParser, get_active_lines, parser
from insights.parsers import SkipException, optlist_to_dict
from insights.specs import Specs

@parser(Specs.ovs_vsctl_list_bridge)
class OVSvsctlListBridge(CommandParser):
    """
    Class to parse output of command ``ovs-vsctl list bridge``.
    Generally, the data is in key:value format with values having
    data types as string, numbers, list or dictionary.
    The class provides attribute ``data`` as list with lines parsed
    line by line based on keys for each bridge.

    Sample command output::

        name                : br-int
        other_config        : {disable-in-band="true", mac-table-size="2048"}
        name                : br-tun
        other_config        : {}

    Examples:
        >>> bridge_lists[0]["name"]
        'br-int'
        >>> bridge_lists[0]["other_config"]["mac-table-size"]
        '2048'
        >>> bridge_lists[0]["other_config"]["disable-in-band"]
        'true'
        >>> bridge_lists[1].get("name")
        'br-tun'
        >>> len(bridge_lists[1]["other_config"]) == 0
        True

    Attributes:
        data (list): A list containing dictionary elements where each
                     element contains the details of a bridge.

    Raises:
        SkipException: When file is empty.
    """
    bridge_keys = ('_uuid', 'auto_attach', 'controller', 'datapath_id', 'datapath_type',
                   'datapath_version', 'external_ids', 'fail_mode', 'flood_vlans',
                   'flow_tables', 'ipfix', 'mcast_snooping_enable:', 'mirrors', 'name',
                   'netflow', 'other_config', 'ports', 'protocols', 'rstp_enable',
                   'rstp_status', 'sflow', 'status', 'stp_enable')

    def parse_content(self, content):
        """
           Details of all the bridges are extracted and stored in a list as dictionary
           elements. Each dictionary element contains the information of a specific
           bridge.
        """
        if not content:
            raise SkipException('Empty file')
        self.data = []
        bridge_details = {}
        for line in get_active_lines(content):
            key, value = [ i.strip() for i in line.split(':', 1) ]
            parsed_value = value.strip('"')
            if value.startswith('{') and value.endswith('}'):
                parsed_value = {}
                value = value.strip('{}')
                if value:
                    parsed_value = optlist_to_dict(value, opt_sep=', ', strip_quotes=True)
            elif value.startswith('[') and value.endswith(']'):
                parsed_value = []
                value = value.strip('[]')
                if value:
                    parsed_value = [ i.strip(' \t"\'') for i in value.split(',') ]
            if key not in bridge_details:
                bridge_details[key] = parsed_value
            else:
                self.data.append(bridge_details)
                bridge_details = {key: parsed_value}

        self.data.append(bridge_details)

    def __getitem__(self, line):
        return self.data[line]