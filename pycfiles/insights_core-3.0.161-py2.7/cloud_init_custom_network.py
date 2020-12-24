# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/cloud_init_custom_network.py
# Compiled at: 2020-03-25 13:10:41
"""
CloudInitCustomeNetwork - file ``/etc/cloud/cloud.cfg.d/99-custom-networking.cfg``
==================================================================================

This module provides parsing for cloudinit custom networking configuration file.
``CloudInitCustomNetworking`` is a parser for ``/etc/cloud/cloud.cfg.d/99-custom-networking.cfg`` files.

Typical output is::

    network:
      version: 1
      config:
      - type: physical
        name: eth0
        subnets:
          - type: dhcp
          - type: dhcp6

Examples:
    >>> cloud_init_custom_network_config.data['network']['config'][0]['name']
    'eth0'
    >>> cloud_init_custom_network_config.data['network']['config'][0]['subnets'][0]['type'] == 'dhcp'
    True
    >>> cloud_init_custom_network_config.data['network']['config'][0]['subnets'][1]['type'] == 'dhcp6'
    True
"""
from insights import YAMLParser, parser
from insights.specs import Specs

@parser(Specs.cloud_init_custom_network)
class CloudInitCustomNetworking(YAMLParser):
    """ Class for parsing the content of ``/etc/cloud/cloud.cfg.d/99-custom-networking.cfg``."""
    pass