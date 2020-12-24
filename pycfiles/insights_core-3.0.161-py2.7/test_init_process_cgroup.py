# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_init_process_cgroup.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import init_process_cgroup
from insights.tests import context_wrap
CGROUP_HOST = ('\n11:hugetlb:/\n10:memory:/\n9:devices:/\n8:pids:/\n7:perf_event:/\n6:net_prio,net_cls:/\n5:blkio:/\n4:freezer:/\n3:cpuacct,cpu:/\n2:cpuset:/\n1:name=systemd:/\n').strip()
CGROUP_CONTAINER = ('\n11:hugetlb:/system.slice/docker-55b2b88feeb4fc56bb9384e55100a8581271ca7a22399c6ec52784a35dba933b.scope\n10:memory:/system.slice/docker-55b2b88feeb4fc56bb9384e55100a8581271ca7a22399c6ec52784a35dba933b.scope\n9:devices:/system.slice/docker-55b2b88feeb4fc56bb9384e55100a8581271ca7a22399c6ec52784a35dba933b.scope\n8:pids:/system.slice/docker-55b2b88feeb4fc56bb9384e55100a8581271ca7a22399c6ec52784a35dba933b.scope\n7:perf_event:/system.slice/docker-55b2b88feeb4fc56bb9384e55100a8581271ca7a22399c6ec52784a35dba933b.scope\n6:net_prio,net_cls:/system.slice/docker-55b2b88feeb4fc56bb9384e55100a8581271ca7a22399c6ec52784a35dba933b.scope\n5:blkio:/system.slice/docker-55b2b88feeb4fc56bb9384e55100a8581271ca7a22399c6ec52784a35dba933b.scope\n4:freezer:/system.slice/docker-55b2b88feeb4fc56bb9384e55100a8581271ca7a22399c6ec52784a35dba933b.scope\n3:cpuacct,cpu:/system.slice/docker-55b2b88feeb4fc56bb9384e55100a8581271ca7a22399c6ec52784a35dba933b.scope\n2:cpuset:/system.slice/docker-55b2b88feeb4fc56bb9384e55100a8581271ca7a22399c6ec52784a35dba933b.scope\n1:name=systemd:/system.slice/docker-55b2b88feeb4fc56bb9384e55100a8581271ca7a22399c6ec52784a35dba933b.scope\n').strip()
CGROUP_CONTAINER_1 = ('\n12:freezer:/machine.slice/libpod-af097fa761cd92daf9ac2e18b6d59959b1212e12621a0951223f9f55d99b452c.scope\n11:pids:/machine.slice/libpod-af097fa761cd92daf9ac2e18b6d59959b1212e12621a0951223f9f55d99b452c.scope\n10:cpuset:/machine.slice/libpod-af097fa761cd92daf9ac2e18b6d59959b1212e12621a0951223f9f55d99b452c.scope\n9:memory:/machine.slice/libpod-af097fa761cd92daf9ac2e18b6d59959b1212e12621a0951223f9f55d99b452c.scope\n8:devices:/machine.slice/libpod-af097fa761cd92daf9ac2e18b6d59959b1212e12621a0951223f9f55d99b452c.scope\n7:blkio:/machine.slice/libpod-af097fa761cd92daf9ac2e18b6d59959b1212e12621a0951223f9f55d99b452c.scope\n6:cpu,cpuacct:/machine.slice/libpod-af097fa761cd92daf9ac2e18b6d59959b1212e12621a0951223f9f55d99b452c.scope\n5:rdma:/\n4:net_cls,net_prio:/machine.slice/libpod-af097fa761cd92daf9ac2e18b6d59959b1212e12621a0951223f9f55d99b452c.scope\n3:perf_event:/machine.slice/libpod-af097fa761cd92daf9ac2e18b6d59959b1212e12621a0951223f9f55d99b452c.scope\n2:hugetlb:/machine.slice/libpod-af097fa761cd92daf9ac2e18b6d59959b1212e12621a0951223f9f55d99b452c.scope\n1:name=systemd:/machine.slice/libpod-af097fa761cd92daf9ac2e18b6d59959b1212e12621a0951223f9f55d99b452c.scope\n').strip()

def test_init_process_cgroup():
    result = init_process_cgroup.InitProcessCgroup(context_wrap(CGROUP_HOST))
    assert result.data['memory'] == ['10', '/']
    assert result.is_container is False
    result = init_process_cgroup.InitProcessCgroup(context_wrap(CGROUP_CONTAINER))
    assert result.data['memory'] == ['10', '/system.slice/docker-55b2b88feeb4fc56bb9384e55100a8581271ca7a22399c6ec52784a35dba933b.scope']
    assert result.is_container is True
    result = init_process_cgroup.InitProcessCgroup(context_wrap(CGROUP_CONTAINER_1))
    assert result.data['memory'] == ['9', '/machine.slice/libpod-af097fa761cd92daf9ac2e18b6d59959b1212e12621a0951223f9f55d99b452c.scope']
    assert result.is_container is True