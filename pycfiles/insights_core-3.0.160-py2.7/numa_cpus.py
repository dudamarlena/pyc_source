# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/numa_cpus.py
# Compiled at: 2019-05-16 13:41:33
"""
NUMACpus - file ``/sys/devices/system/node/node[0-9]*/cpulist``
===============================================================

This parser will parse the content from cpulist file, from individual
NUMA nodes. This parser will return data in (dict) format.

Sample Content from ``/sys/devices/system/node/node0/cpulist``::

    0-6,14-20

Examples:
    >>> type(numa_cpus_obj)
    <class 'insights.parsers.numa_cpus.NUMACpus'>
    >>> numa_cpus_obj.numa_node_name
    'node0'
    >>> numa_cpus_obj.numa_node_details() == {'numa_node_range': ['0-6', '14-20'], 'total_cpus': 14, 'numa_node_name': 'node0'}
    True
    >>> numa_cpus_obj.numa_node_cpus
    ['0-6', '14-20']
    >>> numa_cpus_obj.total_numa_node_cpus
    14
"""
from insights import Parser, parser, LegacyItemAccess
from insights.specs import Specs
from insights.parsers import SkipException

@parser(Specs.numa_cpus)
class NUMACpus(LegacyItemAccess, Parser):
    """
    Parse `/sys/devices/system/node/node[0-9]*/cpulist` file, return a dict
    which contains total number of CPUs per numa node.
    """

    def parse_content(self, content):
        if not content or not self.file_path:
            raise SkipException('No Contents')
        self.data = {}
        self._cpu_ranges = []
        self.numa_node = self.file_path.rsplit('/')[(-2)] if self.file_path else None
        for line in content:
            total_cpus = 0
            self._cpu_ranges = line.split(',')
            self.data['numa_node_range'] = self._cpu_ranges
            self.data['numa_node_name'] = self.numa_node
            if '-' in self._cpu_ranges[0]:
                for cpu_range in self._cpu_ranges:
                    lower_num = int(cpu_range.split('-')[0])
                    higher_num = int(cpu_range.split('-')[1])
                    ncpus = higher_num - lower_num + 1
                    total_cpus = total_cpus + ncpus

            else:
                total_cpus = len(self._cpu_ranges)
            self.data['total_cpus'] = total_cpus

        return

    @property
    def numa_node_name(self):
        """
        (str): It will return the CPU node name when set, else `None`.
        """
        if self.numa_node:
            return self.numa_node
        else:
            return

    @property
    def numa_node_cpus(self):
        """
        (list): It will return list of CPUs present under NUMA node when set, else `None`.
        """
        if self._cpu_ranges:
            return self._cpu_ranges
        else:
            return

    @property
    def total_numa_node_cpus(self):
        """
        (int): It will return total number of CPUs per NUMA node
        """
        if 'total_cpus' in self.data:
            return self.data['total_cpus']
        else:
            return

    def numa_node_details(self):
        """
        (dict): it will return the number of CPUs per NUMA, NUMA node name, CPU range, when set, else `None`.
        """
        if self.data:
            return self.data
        else:
            return