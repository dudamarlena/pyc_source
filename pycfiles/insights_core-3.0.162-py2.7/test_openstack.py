# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/components/tests/test_openstack.py
# Compiled at: 2019-11-14 13:57:46
import pytest
from insights.components.openstack import IsOpenStackCompute
from insights.parsers.ps import PsAuxcww
from insights.tests import context_wrap
from insights.core.dr import SkipComponent
PS_MULTIPATHD = ('\nUSER       PID %CPU %MEM    VSZ   RSS TTY      STAT START    TIME  COMMAND\nroot         9  0.0  0.0      0     0 ?        S    Mar24   0:05  multipathd\n').strip()
PS_OSP_COMPUTE = ('\nUSER       PID %CPU %MEM    VSZ   RSS TTY      STAT START    TIME  COMMAND\nnova     24928  0.1  1.1 390180 89368 ?        Ss   11:30   0:09  nova-compute\nroot         9  0.0  0.0      0     0 ?        S    Mar24   0:05  multipathd\n').strip()
PS_OSP_DIRECTOR = ('\nUSER       PID %CPU %MEM    VSZ   RSS TTY      STAT START    TIME  COMMAND\nnova     24928  0.1  1.1 390180 89368 ?        Ss   11:30   0:09  nova-compute\nnova     24928  0.1  1.1 390180 89368 ?        Ss   11:30   0:09  nova-conductor\nroot         9  0.0  0.0      0     0 ?        S    Mar24   0:05  multipathd\n').strip()
PS_OSP_CONTROLLER = ('\nUSER       PID %CPU %MEM    VSZ   RSS TTY      STAT START    TIME  COMMAND\nnova     24928  0.1  1.1 390180 89368 ?        Ss   11:30   0:09  nova-conductor\nroot         9  0.0  0.0      0     0 ?        S    Mar24   0:05  multipathd\n').strip()

def test_generic_process():
    """The ``psauxcww`` does not have ``nova-compute`` process."""
    ps = PsAuxcww(context_wrap(PS_MULTIPATHD))
    with pytest.raises(SkipComponent) as (e):
        IsOpenStackCompute(ps)
    assert 'Not OpenStack Compute node' in str(e)


def test_compute_node():
    ps = PsAuxcww(context_wrap(PS_OSP_COMPUTE))
    result = IsOpenStackCompute(ps)
    assert isinstance(result, IsOpenStackCompute)


def test_controller_node():
    ps = PsAuxcww(context_wrap(PS_OSP_CONTROLLER))
    with pytest.raises(SkipComponent) as (e):
        IsOpenStackCompute(ps)
    assert 'Not OpenStack Compute node' in str(e)


def test_director_node():
    ps = PsAuxcww(context_wrap(PS_OSP_DIRECTOR))
    result = IsOpenStackCompute(ps)
    assert isinstance(result, IsOpenStackCompute)