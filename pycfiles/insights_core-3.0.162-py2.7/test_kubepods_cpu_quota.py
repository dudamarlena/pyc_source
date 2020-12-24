# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_kubepods_cpu_quota.py
# Compiled at: 2019-05-16 13:41:33
import doctest, pytest
from insights.parsers import kubepods_cpu_quota, ParseException
from insights.parsers.kubepods_cpu_quota import KubepodsCpuQuota
from insights.tests import context_wrap
KUBEPODS_CPU_QUOTA_1 = ('\n-1\n').strip()
KUBEPODS_CPU_QUOTA_2 = ('\n50000\n').strip()
KUBEPODS_CPU_QUOTA_INVALID = ('\ninvalid\n-1\n').strip()

def test_kubepods_cpu_quota():
    cpu_quota = kubepods_cpu_quota.KubepodsCpuQuota(context_wrap(KUBEPODS_CPU_QUOTA_1))
    assert cpu_quota.cpu_quota == -1


def test_kubepods_cpu_quota_2():
    cpu_quota = kubepods_cpu_quota.KubepodsCpuQuota(context_wrap(KUBEPODS_CPU_QUOTA_2))
    assert cpu_quota.cpu_quota == 50000


def test_invalid():
    with pytest.raises(ParseException) as (e):
        kubepods_cpu_quota.KubepodsCpuQuota(context_wrap(KUBEPODS_CPU_QUOTA_INVALID))
    assert 'invalid' in str(e)


def test_akubepods_cpu_quota_doc_examples():
    env = {'kubepods_cpu_quota': KubepodsCpuQuota(context_wrap(KUBEPODS_CPU_QUOTA_1))}
    failed, total = doctest.testmod(kubepods_cpu_quota, globs=env)
    assert failed == 0