# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_cpuset_cpus.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import cpuset_cpus
from insights.tests import context_wrap
CPUSET_CPU = ('\n0,2-4,7\n').strip()

def test_init_process_cgroup():
    cpusetinfo = cpuset_cpus.CpusetCpus(context_wrap(CPUSET_CPU))
    assert cpusetinfo.cpu_set == ['0', '2', '3', '4', '7']
    assert cpusetinfo.cpu_number == 5