# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ndctl_list.py
# Compiled at: 2020-04-16 14:56:28
import doctest
from insights.parsers import ndctl_list
from insights.parsers.ndctl_list import NdctlListNi
from insights.tests import context_wrap
NDCTL_OUTPUT = ('\n[\n    {\n        "dev":"namespace1.0",\n        "mode":"fsdax",\n        "map":"mem",\n        "size":811746721792,\n        "uuid":"6a7d93f5-60c4-461b-8d19-0409bd323a94",\n        "sector_size":512,\n        "align":2097152,\n        "blockdev":"pmem1"\n    },\n    {\n        "dev":"namespace1.1",\n        "mode":"raw",\n        "size":0,\n        "uuid":"00000000-0000-0000-0000-000000000000",\n        "sector_size":512,\n        "state":"disabled"\n    },\n    {\n        "dev":"namespace0.0",\n        "mode":"raw",\n        "size":0,\n        "uuid":"00000000-0000-0000-0000-000000000000",\n        "sector_size":512,\n        "state":"disabled"\n    }\n]\n').strip()

def test_netstat_doc_examples():
    env = {'ndctl_list': NdctlListNi(context_wrap(NDCTL_OUTPUT))}
    failed, total = doctest.testmod(ndctl_list, globs=env)
    assert failed == 0


def test_get_dev_attr():
    ndctl = NdctlListNi(context_wrap(NDCTL_OUTPUT))
    assert ndctl.blockdev_list == ['pmem1']
    assert 'map' in ndctl.get_blockdev('pmem1')
    assert ndctl.get_blockdev('pmem1').get('map') == 'mem'
    assert ndctl.get_blockdev('pmem2') == {}