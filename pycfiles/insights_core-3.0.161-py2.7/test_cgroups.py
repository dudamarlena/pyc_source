# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_cgroups.py
# Compiled at: 2019-05-16 13:41:33
import doctest, pytest
from insights.parsers import cgroups
from insights.parsers.cgroups import Cgroups
from insights.tests import context_wrap
cgroups_content = ('\n#subsys_name\thierarchy\tnum_cgroups\tenabled\ncpuset\t10\t48\t1\ncpu\t2\t232\t1\ncpuacct\t2\t232\t1\nmemory\t5\t232\t1\ndevices\t6\t232\t1\nfreezer\t3\t48\t1\nnet_cls\t4\t48\t1\nblkio\t9\t232\t1\nperf_event\t8\t48\t1\nhugetlb\t11\t48\t1\npids\t7\t232\t1\nnet_prio\t4\t48\t1\n').strip()

def test_cgroups():
    context = context_wrap(cgroups_content)
    i_cgroups = Cgroups(context)
    assert i_cgroups.get_num_cgroups('memory') == 232
    assert i_cgroups.is_subsys_enabled('memory') is True
    assert i_cgroups.subsystems['memory']['enabled'] == '1'
    with pytest.raises(KeyError) as (ke):
        i_cgroups.get_num_cgroups('Wrong_memory')
    assert 'wrong subsys_name' in str(ke)


def test_cgroup_documentation():
    env = {'i_cgroups': Cgroups(context_wrap(cgroups_content))}
    failed, total = doctest.testmod(cgroups, globs=env)
    assert failed == 0