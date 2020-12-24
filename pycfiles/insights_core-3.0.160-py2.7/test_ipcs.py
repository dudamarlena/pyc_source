# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ipcs.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import ipcs, ParseException, SkipException
from insights.parsers.ipcs import IpcsS, IpcsSI, IpcsM, IpcsMP
from insights.tests import context_wrap
import pytest, doctest
IPCS_S = ('\n------ Semaphore Arrays --------\nkey        semid      owner      perms      nsems\n0x00000000 557056     apache     600        1\n0x00000000 589825     apache     600        1\n0x00000000 131074     apache     600        1\n0x0052e2c1 163843     postgres   600        17\n0x0052e2c2 196612     postgres   600        17\n0x0052e2c3 229381     postgres   600        17\n0x0052e2c4 262150     postgres   600        17\n0x0052e2c5 294919     postgres   600        17\n0x0052e2c6 327688     postgres   600        17\n0x0052e2c7 360457     postgres   600        17\n0x00000000 622602     apache     600        1\n0x00000000 655371     apache     600        1\n0x00000000 688140     apache     600        1\n').strip()
IPCS_S_I = ('\nSemaphore Array semid=65536\nuid=500  gid=501     cuid=500    cgid=501\nmode=0600, access_perms=0600\nnsems = 8\notime = Sun May 12 14:44:53 2013\nctime = Wed May  8 22:12:15 2013\nsemnum     value      ncount     zcount     pid\n0          1          0          0          0\n1          1          0          0          0\n0          1          0          0          6151\n3          1          0          0          2265\n4          1          0          0          0\n5          1          0          0          0\n0          0          7          0          6152\n7          1          0          0          4390\n').strip()
IPCS_M = ('\n------ Shared Memory Segments --------\nkey        shmid      owner      perms      bytes      nattch     status\n0x0052e2c1 0          postgres   600        37879808   26\n0x0052e2c2 1          postgres   600        41222144   24\n').strip()
IPCS_M_P = ('\n------ Shared Memory Creator/Last-op --------\nshmid      owner      cpid       lpid\n0          postgres   1833       23566\n1          postgres   1105       9882\n').strip()
IPCS_M_AB = ('\n------ Shared Memory Segments --------\nkey        shid      owner      perms      bytes      nattch     status\n0x0052e2c1 0          postgres   600        37879808   26\n0x0052e2c2 1          postgres   600        41222144   24\n').strip()

def test_ipcs_s():
    sem = IpcsS(context_wrap(IPCS_S))
    assert '131074' in sem
    assert '11074' not in sem
    assert sem.get('262150') == {'owner': 'postgres', 'perms': '600', 'nsems': '17', 
       'key': '0x0052e2c4'}
    assert sem['622602'] == {'owner': 'apache', 'perms': '600', 'nsems': '1', 
       'key': '0x00000000'}


def test_ipcs_si():
    sem = IpcsSI(context_wrap(IPCS_S_I))
    assert sem.semid == '65536'
    assert sem.pid_list == ['0', '2265', '4390', '6151', '6152']


def test_ipcs_m():
    shm = IpcsM(context_wrap(IPCS_M))
    assert '1' in shm
    assert '0' in shm
    assert '11074' not in shm
    assert shm.get('0').get('bytes') == '37879808'


def test_ipcs_mp():
    shm = IpcsMP(context_wrap(IPCS_M_P))
    assert '1' in shm
    assert '1074' not in shm
    assert shm.get('1').get('cpid') == '1105'


def test_ipcs_abnormal():
    with pytest.raises(SkipException) as (pe):
        IpcsMP(context_wrap(''))
    assert 'Nothing to parse.' in str(pe)
    with pytest.raises(ParseException) as (pe):
        IpcsMP(context_wrap(IPCS_M_AB))
    assert 'Unexpected heading line.' in str(pe)


def test_doc_examples():
    env = {'sem': IpcsS(context_wrap(IPCS_S)), 
       'semi': IpcsSI(context_wrap(IPCS_S_I)), 
       'shm': IpcsM(context_wrap(IPCS_M)), 
       'shmp': IpcsMP(context_wrap(IPCS_M_P))}
    failed, total = doctest.testmod(ipcs, globs=env)
    assert failed == 0