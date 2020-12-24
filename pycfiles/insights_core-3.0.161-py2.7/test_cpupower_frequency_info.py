# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_cpupower_frequency_info.py
# Compiled at: 2019-11-14 13:57:46
import doctest, pytest
from insights.parsers import cpupower_frequency_info, ParseException, SkipException
from insights.parsers.cpupower_frequency_info import CpupowerFrequencyInfo
from insights.tests import context_wrap
CPUPOWER_INFO = ('\nanalyzing CPU 0:\n  test:\n    test_key1: value1\n    test2:\n      test_key2: value2\n        test3:\n          test_key3: value3\n  driver: pcc-cpufreq\n  CPUs which run at the same hardware frequency: 0\n  CPUs which need to have their frequency coordinated by software: 0\n  maximum transition latency:  Cannot determine or is not supported.\n  hardware limits: 1.20 GHz - 2.20 GHz\n  available cpufreq governors: conservative userspace powersave ondemand performance\n  current policy: frequency should be within 1.20 GHz and 2.20 GHz.\n                  The governor "performance" may decide which speed to use\n                  within this range.\n  current CPU frequency: 2.38 GHz (asserted by call to hardware)\n  boost state support:\n    Supported: yes\n    Active: yes\n    2700 MHz max turbo 4 active cores\n    2800 MHz max turbo 3 active cores\n    2900 MHz max turbo 2 active cores\n    3000 MHz max turbo 1 active cores\n').strip()
CPUPOWER_INFO_MULTI = '\nanalyzing CPU 0:\n  driver: intel_pstate\n  CPUs which run at the same hardware frequency: 0\n  CPUs which need to have their frequency coordinated by software: 0\n  maximum transition latency:  Cannot determine or is not supported.\n  hardware limits: 800 MHz - 3.00 GHz\n  available cpufreq governors: performance powersave\n  current policy: frequency should be within 800 MHz and 3.00 GHz.\n                  The governor "performance" may decide which speed to use\n                  within this range.\n  current CPU frequency: Unable to call hardware\n  current CPU frequency: 1.22 GHz (asserted by call to kernel)\n  boost state support:\n    Supported: yes\n    Active: yes\n    2700 MHz max turbo 4 active cores\n    2800 MHz max turbo 3 active cores\n    2900 MHz max turbo 2 active cores\n    3000 MHz max turbo 1 active cores\nanalyzing CPU 1:\n  driver: intel_pstate\n  CPUs which run at the same hardware frequency: 1\n  CPUs which need to have their frequency coordinated by software: 1\n  maximum transition latency:  Cannot determine or is not supported.\n  hardware limits: 800 MHz - 3.00 GHz\n  available cpufreq governors: performance powersave\n  current policy: frequency should be within 800 MHz and 3.00 GHz.\n                  The governor "performance" may decide which speed to use\n                  within this range.\n  current CPU frequency: Unable to call hardware\n  current CPU frequency: 1.22 GHz (asserted by call to kernel)\n  boost state support:\n    Supported: yes\n    Active: yes\nanalyzing CPU 2:\n  driver: intel_pstate\n  CPUs which run at the same hardware frequency: 2\n  CPUs which need to have their frequency coordinated by software: 2\n  maximum transition latency:  Cannot determine or is not supported.\n  hardware limits: 800 MHz - 3.00 GHz\n  available cpufreq governors: performance powersave\n  current policy: frequency should be within 800 MHz and 3.00 GHz.\n                  The governor "performance" may decide which speed to use\n                  within this range.\n  current CPU frequency: Unable to call hardware\n  current CPU frequency: 871 MHz (asserted by call to kernel)\n  boost state support:\n    Supported: yes\n    Active: yes\nanalyzing CPU 3:\n  driver: intel_pstate\n  CPUs which run at the same hardware frequency: 3\n  CPUs which need to have their frequency coordinated by software: 3\n  maximum transition latency:  Cannot determine or is not supported.\n  hardware limits: 800 MHz - 3.00 GHz\n  available cpufreq governors: performance powersave\n  current policy: frequency should be within 800 MHz and 3.00 GHz.\n                  The governor "performance" may decide which speed to use\n                  within this range.\n  current CPU frequency: Unable to call hardware\n  current CPU frequency: 868 MHz (asserted by call to kernel)\n  boost state support:\n    Supported: yes\n    Active: yes\n'
CPUPOWER_INFO_INVALID = ('\nERROR FIRST LINE:\n  driver: pcc-cpufreq\n  CPUs which run at the same hardware frequency: 0\n  CPUs which need to have their frequency coordinated by software: 0\n  maximum transition latency:  Cannot determine or is not supported.\n  hardware limits: 1.20 GHz - 2.20 GHz\n  available cpufreq governors: conservative userspace powersave ondemand performance\n  current policy: frequency should be within 1.20 GHz and 2.20 GHz.\n                  The governor "performance" may decide which speed to use\n                  within this range.\n  current CPU frequency: 2.38 GHz (asserted by call to hardware)\n  boost state support:\n    Supported: yes\n    Active: yes\n    2700 MHz max turbo 4 active cores\n    2800 MHz max turbo 3 active cores\n    2900 MHz max turbo 2 active cores\n    3000 MHz max turbo 1 active cores\n').strip()
CPUPOWER_INFO_EMPTY = ('\n').strip()

def test_cpupower_frequency_info():
    cpupower_info = CpupowerFrequencyInfo(context_wrap(CPUPOWER_INFO))
    assert cpupower_info['analyzing CPU 0']['boost state support']['Supported'] == 'yes'
    assert cpupower_info['analyzing CPU 0']['boost state support']['Active'] == 'yes'
    assert cpupower_info['analyzing CPU 0']['current policy'] == 'frequency should be within 1.20 GHz and 2.20 GHz. The governor "performance" may decide which speed to use within this range.'
    assert cpupower_info['analyzing CPU 0']['boost state support']['2700 MHz max turbo 4 active cores'] is True


def test_cpupower_frequency_info_multi():
    cpupower_info = CpupowerFrequencyInfo(context_wrap(CPUPOWER_INFO_MULTI))
    assert cpupower_info['analyzing CPU 3']['boost state support']['Supported'] == 'yes'
    assert cpupower_info['analyzing CPU 3']['boost state support']['Active'] == 'yes'
    assert cpupower_info['analyzing CPU 3']['current policy'] == 'frequency should be within 800 MHz and 3.00 GHz. The governor "performance" may decide which speed to use within this range.'


def test_invalid():
    with pytest.raises(ParseException) as (e):
        CpupowerFrequencyInfo(context_wrap(CPUPOWER_INFO_INVALID))
    assert 'Incorrect content' in str(e)


def test_empty():
    with pytest.raises(SkipException) as (e):
        CpupowerFrequencyInfo(context_wrap(CPUPOWER_INFO_EMPTY))
    assert 'Empty content' in str(e)


def test_cpupower_frequency_info_doc_examples():
    env = {'cpupower_frequency_info': CpupowerFrequencyInfo(context_wrap(CPUPOWER_INFO_MULTI))}
    failed, total = doctest.testmod(cpupower_frequency_info, globs=env)
    assert failed == 0