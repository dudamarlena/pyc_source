# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_ipcs_shared_memory.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import ParseException
from insights.parsers.ipcs import IpcsM, IpcsMP
from insights.combiners import ipcs_shared_memory
from insights.combiners.ipcs_shared_memory import IpcsSharedMemory
from insights.tests import context_wrap
import doctest, pytest
IPCS_M = ('\n------ Shared Memory Segments --------\nkey        shmid      owner      perms      bytes      nattch     status\n0x0052e2c1 0          postgres   600        37879808   26\n0x0052e2c2 1          postgres   600        41222144   24\n').strip()
IPCS_M_P = ('\n------ Shared Memory Creator/Last-op --------\nshmid      owner      cpid       lpid\n0          postgres   1833       23566\n1          postgres   1105       9882\n').strip()
IPCS_M_P_AB = ('\n------ Shared Memory Creator/Last-op --------\nshmid      owner      cpid       lpid\n0          postgres   1833       23566\n').strip()

def test_ipcs_shm():
    shm = IpcsM(context_wrap(IPCS_M))
    shmp = IpcsMP(context_wrap(IPCS_M_P))
    rst = IpcsSharedMemory(shm, shmp)
    assert rst.get_shm_size_of_pid('1833') == 37879808
    assert rst.get_shm_size_of_pid('33') == 0


def test_ipcs_shm_abnormal():
    shm = IpcsM(context_wrap(IPCS_M))
    shmp = IpcsMP(context_wrap(IPCS_M_P_AB))
    with pytest.raises(ParseException) as (pe):
        IpcsSharedMemory(shm, shmp)
    assert "The output of 'ipcs -m' doesn't match with 'ipcs -m -p'." in str(pe)


def test_doc_examples():
    env = {'ism': IpcsSharedMemory(IpcsM(context_wrap(IPCS_M)), IpcsMP(context_wrap(IPCS_M_P)))}
    failed, total = doctest.testmod(ipcs_shared_memory, globs=env)
    assert failed == 0