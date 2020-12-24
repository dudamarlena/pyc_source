# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_lscpu.py
# Compiled at: 2019-11-14 13:57:46
import doctest, pytest
from insights.parsers import lscpu, SkipException
from insights.tests import context_wrap
LSCPU_1 = ('\nArchitecture:          x86_64\nCPU op-mode(s):        32-bit, 64-bit\nByte Order:            Little Endian\nCPU(s):                2\nOn-line CPU(s) list:   0,1\nThread(s) per core:    2\nCore(s) per socket:    1\nSocket(s):             1\nNUMA node(s):          1\nVendor ID:             GenuineIntel\nCPU family:            6\nModel:                 60\nModel name:            Intel Core Processor (Haswell, no TSX)\nStepping:              1\nCPU MHz:               2793.530\nBogoMIPS:              5587.06\nHypervisor vendor:     KVM\nVirtualization type:   full\nL1d cache:             32K\nL1i cache:             32K\nL2 cache:              4096K\nNUMA node0 CPU(s):     0,1\n').strip()
LSCPU_2 = ('\nArchitecture:          x86_64\nCPU op-mode(s):        32-bit, 64-bit\nByte Order:            Little Endian\nCPU(s):                2\nOn-line CPU(s) list:   0\nOff-line CPU(s) list:  1\nThread(s) per core:    1\nCore(s) per socket:    1\nSocket(s):             1\nNUMA node(s):          1\nVendor ID:             GenuineIntel\nCPU family:            6\nModel:                 60\nModel name:            Intel Core Processor (Haswell, no TSX)\nStepping:              1\nCPU MHz:               2793.530\nBogoMIPS:              5587.06\nHypervisor vendor:     KVM\nVirtualization type:   full\nL1d cache:             32K\nL1i cache:             32K\nL2 cache:              4096K\nNUMA node0 CPU(s):     0\n').strip()
BLANK = ('\n').strip()
BAD_LSCPU = ('\nArchitecture:          x86_64\nCPU op-mode(s) =        32-bit, 64-bit\n').strip()

def test_lscpu_output():
    output = lscpu.LsCPU(context_wrap(LSCPU_1))
    assert output.info['Architecture'] == 'x86_64'
    assert len(output.info) == 22
    assert output.info['CPUs'] == '2'
    assert output.info['Threads per core'] == '2'
    assert output.info['Cores per socket'] == '1'
    assert output.info['Sockets'] == '1'
    output = lscpu.LsCPU(context_wrap(LSCPU_2))
    assert output.info['Architecture'] == 'x86_64'
    assert output.info['CPUs'] == '2'
    assert output.info['On-line CPUs list'] == '0'
    assert output.info['Off-line CPUs list'] == '1'
    assert output.info['Cores per socket'] == '1'
    assert output.info['Sockets'] == '1'


def test_lscpu_blank_output():
    with pytest.raises(SkipException) as (e):
        lscpu.LsCPU(context_wrap(BLANK))
    assert 'No data.' in str(e)


def test_documentation():
    failed_count, tests = doctest.testmod(lscpu, globs={'output': lscpu.LsCPU(context_wrap(LSCPU_1))})
    assert failed_count == 0