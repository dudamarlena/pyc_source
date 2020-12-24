# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_virsh_list_all.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import virsh_list_all
from insights.tests import context_wrap
BLANK = ('\n').strip()
NO_RESULT = ('\n Id    Name                           State\n----------------------------------------------------\n').strip()
OUTPUT = ('\n Id    Name                           State\n----------------------------------------------------\n 2     rhel7.4                        running\n 4     rhel7.0                        paused\n -     centos6.8-router               shut off\n -     cfme-5.7.13                    shut off\n -     cfme-rhos-5.9.0.15             shut off\n -     fedora-24-kernel               shut off\n -     fedora-saio_fedoraSaio         shut off\n -     fedora24-misc                  shut off\n -     freebsd11.0                    shut off\n -     guixSD                         shut off\n -     miq-gap-1                      shut off\n -     rhel7.2                        shut off\n -     RHOSP10                        shut off\n').strip()

def test_virsh_output():
    output = virsh_list_all.VirshListAll(context_wrap(OUTPUT))
    assert len(output.search(state='shut off')) == 11
    assert len(output.search(id=None)) == 11
    assert len(output.search(id=2)) == 1
    assert output.search(name='rhel7.4') == [{'state': 'running', 'id': 2, 'name': 'rhel7.4'}]
    assert output.get_vm_state('rhel7.0') == 'paused'
    assert output.get_vm_state('rhel9.0') is None
    assert ('cfme' in output) is False
    assert ('cfme-5.7.13' in output) is True
    return


def test_virsh_output_no_vms():
    output = virsh_list_all.VirshListAll(context_wrap(NO_RESULT))
    assert output.fields == []
    assert output.cols == []
    assert output.keywords == []
    assert output.get_vm_state('NORHEL') is None
    return


def test_virsh_output_blank():
    output = virsh_list_all.VirshListAll(context_wrap(BLANK))
    assert output.fields == []
    assert output.cols == []
    assert output.keywords == []
    assert output.get_vm_state('NORHEL') is None
    return


def test_virsh_list_all_documentation():
    failed_count, tests = doctest.testmod(virsh_list_all, globs={'output': virsh_list_all.VirshListAll(context_wrap(OUTPUT))})
    assert failed_count == 0