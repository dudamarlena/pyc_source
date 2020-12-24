# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_virt_what.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.virt_what import VirtWhat
from insights.tests import context_wrap
errors = ['virt-what: virt-what-cpuid-helper program not found in $PATH']
VW_OUT1 = ('\nkvm\n').strip()
VW_OUT2 = ('\n\n').strip()
VW_OUT3 = ('\nxen\nxen-dom0\naws\n').strip()

def test_kvm():
    v1 = VirtWhat(context_wrap(VW_OUT1))
    assert v1.is_virtual is True
    assert v1.generic == 'kvm'
    assert v1.specifics == []
    assert v1.errors == []


def test_bEaR_metal():
    v2 = VirtWhat(context_wrap(VW_OUT2))
    assert v2.is_physical is True
    assert v2.generic == 'baremetal'
    assert v2.specifics == []
    assert v2.errors == []


def test_xen():
    v3 = VirtWhat(context_wrap(VW_OUT3))
    assert v3.is_virtual is True
    assert v3.generic == 'xen'
    assert 'xen-dom0' in v3
    assert 'xen' in v3
    assert 'aws' in v3
    assert v3.errors == []


def test_error_handling():
    v = VirtWhat(context_wrap(errors[0]))
    assert v.generic == ''
    assert v.specifics == []
    assert v.is_virtual is None
    assert v.is_physical is None
    assert v.errors == errors
    return