# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_cpu_vulns.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers import SkipException
from insights.tests import context_wrap
from insights.parsers import cpu_vulns
from insights.parsers.cpu_vulns import CpuVulns
import pytest, doctest
INPUT_MELTDOWN = ('\nMitigation: PTI\n').strip()
INPUT_SPECTRE_V1 = ('\nMitigation: Load fences\n').strip()
INPUT_SPECTRE_V2_RHEL_7_1 = ('\nMitigation: Full generic retpoline, IBPB: conditional, IBRS_FW, STIBP: conditional, RSB filling\n').strip()
INPUT_SPECTRE_V2_RHEL_7 = ('\nVulnerable: Retpoline without IBPB\n').strip()
INPUT_SPECTRE_V2_RHEL_6 = ('\nMitigation: IBRS (kernel)\n').strip()
INPUT_SPEC_STORE_BYPASS = ('\nMitigation: Speculative Store Bypass disabled\n').strip()
INPUT_SPEC_STORE_BYPASS_2 = ('\nNot affected\n').strip()
INPUT_SPEC_STORE_BYPASS_3 = ('\nVulnerable\n').strip()
INPUT_SMT = ('\nMitigation: PTE Inversion; VMX: conditional cache flushes, SMT vulnerable\n').strip()
INPUT_MDS = ('\nVulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable\n').strip()
INPUT_MDS_2 = ('\nNot affected\n').strip()
INPUT_MDS_3 = ('\nMitigation: Clear CPU buffers; SMT vulnerable\n').strip()
INPUT_MDS_4 = ('\nMitigation: Clear CPU buffers; SMT disabled\n').strip()
INPUT_MDS_5 = ('\nMitigation: Clear CPU buffers; SMT Host state unknown\n').strip()

def test_cpu_vulns_meltdown():
    spectre = CpuVulns(context_wrap(INPUT_MELTDOWN, path='/sys/devices/system/cpu/vulnerabilities/meltdown'))
    assert spectre.value == INPUT_MELTDOWN
    assert spectre.file_name == 'meltdown'


def test_cpu_vulns_meltdown_exp1():
    """
    Here test the examples cause expections
    """
    with pytest.raises(SkipException) as (sc1):
        CpuVulns(context_wrap('', path='/sys/devices/system/cpu/vulnerabilities/meltdown'))
    assert 'Input content is empty' in str(sc1)


def test_cpu_vulns_spec_store_bypass():
    spectre = CpuVulns(context_wrap(INPUT_SPEC_STORE_BYPASS, path='/sys/devices/system/cpu/vulnerabilities/spec_store_bypass'))
    assert spectre.value == INPUT_SPEC_STORE_BYPASS
    assert spectre.file_name == 'spec_store_bypass'


def test_cpu_vulns_spec_store_bypass_2():
    spectre = CpuVulns(context_wrap(INPUT_SPEC_STORE_BYPASS_2, path='/sys/devices/system/cpu/vulnerabilities/spec_store_bypass'))
    assert spectre.value == INPUT_SPEC_STORE_BYPASS_2
    assert spectre.file_name == 'spec_store_bypass'


def test_cpu_vulns_spec_store_bypass_3():
    spectre = CpuVulns(context_wrap(INPUT_SPEC_STORE_BYPASS_3, path='/sys/devices/system/cpu/vulnerabilities/spec_store_bypass'))
    assert spectre.value == INPUT_SPEC_STORE_BYPASS_3
    assert spectre.file_name == 'spec_store_bypass'


def test_cpu_vulns_spec_store_bypass_exp1():
    """
    Here test the examples cause expections
    """
    with pytest.raises(SkipException) as (sc1):
        CpuVulns(context_wrap('', path='meltdown'))
    assert 'Input content is empty' in str(sc1)


def test_cpu_vulns_spectre_v1():
    spectre = CpuVulns(context_wrap(INPUT_SPECTRE_V1, path='/sys/devices/system/cpu/vulnerabilities/spectre_v1'))
    assert spectre.value == INPUT_SPECTRE_V1
    assert spectre.file_name == 'spectre_v1'


def test_cpu_vulns_spectre_v1_exp1():
    """
    Here test the examples cause expections
    """
    with pytest.raises(SkipException) as (sc1):
        CpuVulns(context_wrap(''))
    assert 'Input content is empty' in str(sc1)


def test_cpu_vulns_spectre_v2_rhel7():
    """
    Here test the examples for spectre_v2
    """
    spectre = CpuVulns(context_wrap(INPUT_SPECTRE_V2_RHEL_7, path='/sys/devices/system/cpu/vulnerabilities/spectre_v2'))
    assert spectre.value == INPUT_SPECTRE_V2_RHEL_7
    assert spectre.file_name == 'spectre_v2'


def test_cpu_vulns_spectre_v2_rhel6():
    """
    Here test the examples for spectre_v2
    """
    spectre = CpuVulns(context_wrap(INPUT_SPECTRE_V2_RHEL_6, path='/sys/devices/system/cpu/vulnerabilities/spectre_v2'))
    assert spectre.value == INPUT_SPECTRE_V2_RHEL_6
    assert spectre.file_name == 'spectre_v2'


def test_cpu_vulns_spectre_v2_exp1():
    """
    Here test the examples cause expections
    """
    with pytest.raises(SkipException) as (sc1):
        CpuVulns(context_wrap(''))
    assert 'Input content is empty' in str(sc1)


def test_cpu_vulns_documentation():
    """
    Here we test the examples in the documentation automatically using doctest.
    We set up an environment which is similar to what a rule writer might see -
    a '/sys/devices/system/cpu/vulnerabilities/*' output that has been
    passed in as a parameter to the rule declaration.
    """
    env = {'sp_v1': CpuVulns(context_wrap(INPUT_SPECTRE_V1, path='/sys/devices/system/cpu/vulnerabilities/spectre_v1')), 
       'sp_v2': CpuVulns(context_wrap(INPUT_SPECTRE_V2_RHEL_7, path='/sys/devices/system/cpu/vulnerabilities/spectre_v2')), 
       'md': CpuVulns(context_wrap(INPUT_MELTDOWN, path='/sys/devices/system/cpu/vulnerabilities/meltdown')), 
       'ssb': CpuVulns(context_wrap(INPUT_SPEC_STORE_BYPASS, path='/sys/devices/system/cpu/vulnerabilities/spec_store_bypass'))}
    failed, total = doctest.testmod(cpu_vulns, globs=env)
    assert failed == 0