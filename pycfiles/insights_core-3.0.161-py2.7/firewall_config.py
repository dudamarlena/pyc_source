# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/firewall_config.py
# Compiled at: 2020-03-25 13:10:41
"""
FirewallDConf - file ``/etc/firewalld/firewalld.conf``
======================================================

The FirewallDConf class parses the file ``/etc/firewalld/firewalld.conf``.
And returns a dict contains the firewall configurations.

Examples:

    >>> type(firewalld)
    <class 'insights.parsers.firewall_config.FirewallDConf'>
    >>> 'DefaultZone' in firewalld
    True
    >>> firewalld['DefaultZone']
    'public'
"""
from insights.specs import Specs
from insights import Parser, parser
from insights.parsers import split_kv_pairs
from insights.parsers import SkipException

@parser(Specs.firewalld_conf)
class FirewallDConf(Parser, dict):
    """
    Class for parsing ``/etc/firewalld/firewalld.conf`` file.
    """

    def parse_content(self, content):
        self.update(split_kv_pairs(content, use_partition=False))
        if not self:
            raise SkipException('empty content')