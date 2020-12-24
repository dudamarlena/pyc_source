# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_smt.py
# Compiled at: 2020-03-25 13:10:41
import doctest, pytest
from insights.parsers import smt, SkipException
from insights.parsers.smt import CpuSMTActive, CpuCoreOnline, CpuSiblings
from insights.tests import context_wrap

def test_cpu_smt_active():
    with pytest.raises(SkipException):
        CpuSMTActive(context_wrap(''))
    p = CpuSMTActive(context_wrap('1'))
    assert p.on
    p = CpuSMTActive(context_wrap('0'))
    assert not p.on


def test_cpu_core_online():
    with pytest.raises(SkipException):
        CpuCoreOnline(context_wrap(''))
    path = '/sys/devices/system/cpu/cpu{0}/online'
    p = CpuCoreOnline(context_wrap('0', path=path.format(0)))
    assert p.core_id == 0
    assert not p.on
    assert repr(p) == '[Core 0: Offline]'
    p = CpuCoreOnline(context_wrap('1', path=path.format(1)))
    assert p.core_id == 1
    assert p.on
    assert repr(p) == '[Core 1: Online]'


def test_cpu_siblings():
    with pytest.raises(SkipException):
        CpuSiblings(context_wrap(''))
    path = '/sys/devices/system/cpu/cpu{0}/topology/thread_siblings_list'
    p = CpuSiblings(context_wrap('0,2', path=path.format(0)))
    assert p.core_id == 0
    assert p.siblings == [0, 2]
    assert repr(p) == '[Core 0 Siblings: [0, 2]]'
    p = CpuSiblings(context_wrap('1-3', path=path.format(3)))
    assert p.core_id == 3
    assert p.siblings == [1, 2, 3]
    assert repr(p) == '[Core 3 Siblings: [1, 2, 3]]'
    p = CpuSiblings(context_wrap('1', path=path.format(1)))
    assert p.core_id == 1
    assert p.siblings == [1]
    assert repr(p) == '[Core 1 Siblings: [1]]'


def test_doc_examples():
    path_cpu_core_online = '/sys/devices/system/cpu/cpu0/online'
    path_cpu_siblings = '/sys/devices/system/cpu/cpu0/topology/thread_siblings_list'
    env = {'cpu_smt': CpuSMTActive(context_wrap('1')), 
       'cpu_core': CpuCoreOnline(context_wrap('1', path=path_cpu_core_online)), 
       'cpu_siblings': CpuSiblings(context_wrap('0,2', path=path_cpu_siblings))}
    failed, total = doctest.testmod(smt, globs=env)
    assert failed == 0