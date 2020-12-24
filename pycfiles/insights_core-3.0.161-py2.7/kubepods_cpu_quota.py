# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/kubepods_cpu_quota.py
# Compiled at: 2019-05-16 13:41:33
"""
KubepodsCpuQuota - CPU quota for each Kubernetes pod
====================================================

This parser reads the content of ``/sys/fs/cgroup/cpu/kubepods.slice/kubepods-burstable.slice/*.slice/cpu.cfs_quota_us``.
"""
from insights import Parser, parser
from insights.specs import Specs
from ..parsers import ParseException

@parser(Specs.kubepods_cpu_quota)
class KubepodsCpuQuota(Parser):
    """
    Class ``KubepodsCpuQuota`` parses the content of the ``/sys/fs/cgroup/cpu/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-pod*.slice/cpu.cfs_quota_us``.

    Attributes:
        cpu_quota (int): It is used to show the value of cpu quota for a particular pod in a Kubernetes cluster or an OpenShift cluster.

    A typical sample of the content of this file looks like::

        -1

    Examples:
        >>> type(kubepods_cpu_quota)
        <class 'insights.parsers.kubepods_cpu_quota.KubepodsCpuQuota'>
        >>> kubepods_cpu_quota.cpu_quota
        -1
    """

    def parse_content(self, content):
        if len(content) != 1 or not content[0].strip('-').isdigit():
            raise ParseException('Error: ', content if content else 'empty file')
        self.cpu_quota = int(content[0].strip())