# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/dnsmasq_conf_all.py
# Compiled at: 2019-11-14 13:57:46
"""
DnsmasqConfAll - files ``/etc/dnsmasq.conf`` and ``/etc/dnsmasq.d/*.conf``
==========================================================================

Combiner for dnsmasq comfiguration files.

The man page http://www.thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html
states that dnsmasq reads /etc/dnsmasq.conf at startup, if it
exists. If conf-dir in dnsmasq.conf specified, then reads files in the
given directory by conf-dir option.

Configurations from *.conf files in the directory /etc/dnsmasq.d/ applied
when conf-dir set to:

conf-dir=/etc/dnsmasq.d
conf-dir=/etc/dnsmasq.d/,*.conf

"""
import os, operator
from fnmatch import fnmatch
from insights.core.plugins import combiner
from insights.core import ConfigCombiner
from insights.parsers.dnsmasq_config import DnsmasqConf
from insights.parsr.query import eq

@combiner(DnsmasqConf)
class DnsmasqConfTree(ConfigCombiner):

    def __init__(self, confs):
        include = eq('conf-dir')
        main_file = 'dnsmasq.conf'
        super(DnsmasqConfTree, self).__init__(confs, main_file, include)

    def find_matches(self, confs, pattern):
        results = []
        if ',' in pattern:
            pattern_split = pattern.split(',')
            if '.conf' in pattern_split[1:]:
                return results
            pattern = pattern_split[0]
        if os.path.dirname(pattern):
            pattern = os.path.join(pattern, '*')
        for c in confs:
            if fnmatch(c.file_path, pattern):
                results.append(c)

        return sorted(results, key=operator.attrgetter('file_name'))

    @property
    def conf_path(self):
        return '/etc/dnsmasq.d'