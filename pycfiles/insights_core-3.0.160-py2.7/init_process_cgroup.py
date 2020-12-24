# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/init_process_cgroup.py
# Compiled at: 2019-05-16 13:41:33
"""
InitProcessCgroup - File ``/proc/1/cgroup``
===========================================

This parser reads the content of ``/proc/1/cgroup``.
This file shows the cgroup detail of init process.
The format of the content is like key-value. We can
also use this info to check if the archive is from
container or host.
"""
from .. import parser, CommandParser, LegacyItemAccess
from insights.specs import Specs

@parser(Specs.init_process_cgroup)
class InitProcessCgroup(CommandParser, LegacyItemAccess):
    """
    Class ``InitProcessCgroup`` parses the content of the ``/proc/1/cgroup``.

    Attributes:

        is_container (bool): It is used to check if a archive is from host or container.
            Return True if the archive is from container.

    A small sample of the content of this file looks like::

        11:hugetlb:/
        10:memory:/
        9:devices:/
        8:pids:/
        7:perf_event:/
        6:net_prio,net_cls:/
        5:blkio:/
        4:freezer:/
        3:cpuacct,cpu:/
        2:cpuset:/
        1:name=systemd:/

    Examples:
        >>> type(cgroupinfo)
        <class 'insights.parsers.init_process_cgroup.InitProcessCgroup'>
        >>> cgroupinfo["memory"]
        ["10", "/"]
        >>> cgroupinfo.is_container
        False
    """

    def parse_content(self, content):
        self.data = {}
        self.is_container = False
        for line in content:
            values = line.split(':')
            self.data[values[1]] = [values[0], values[2]]
            if 'system.slice/docker-' in values[2] or 'machine.slice/libpod-' in values[2]:
                self.is_container = True