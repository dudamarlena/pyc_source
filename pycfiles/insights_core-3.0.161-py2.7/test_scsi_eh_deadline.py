# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_scsi_eh_deadline.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import scsi_eh_deadline
from insights.parsers.scsi_eh_deadline import SCSIEhDead
from insights.tests import context_wrap
SCSI_HOST0_PATH = '/sys/class/scsi_host/host0/eh_deadline'
SCSI_HOSTS_0 = ('\noff\n').strip()
SCSI_HOST1_PATH = '/sys/class/scsi_host/host1/eh_deadline'
SCSI_HOSTS_1 = ('\n10\n').strip()
SCSI_HOST2_PATH = '/sys/class/scsi_host/host2/eh_deadline'
SCSI_HOSTS_2 = ('\n-1\n').strip()

def test_scsi_eh_deadline_host0():
    context = context_wrap(SCSI_HOSTS_0, SCSI_HOST0_PATH)
    r = SCSIEhDead(context)
    assert r.scsi_host == 'host0'
    assert r.host_eh_deadline == 'off'
    assert r.data == {'host0': 'off'}


def test_scsi_eh_deadline_host1():
    context = context_wrap(SCSI_HOSTS_1, SCSI_HOST1_PATH)
    r = SCSIEhDead(context)
    assert r.scsi_host == 'host1'
    assert r.host_eh_deadline == '10'
    assert r.data == {'host1': '10'}


def test_scsi_eh_deadline_host2():
    context = context_wrap(SCSI_HOSTS_2, SCSI_HOST2_PATH)
    r = SCSIEhDead(context)
    assert r.scsi_host == 'host2'
    assert r.host_eh_deadline == '-1'
    assert r.data == {'host2': '-1'}


def test_scsi_fwver_doc_examples():
    env = {'scsi_obj0': SCSIEhDead(context_wrap(SCSI_HOSTS_0, SCSI_HOST0_PATH)), 
       'scsi_obj1': SCSIEhDead(context_wrap(SCSI_HOSTS_1, SCSI_HOST1_PATH)), 
       'scsi_obj2': SCSIEhDead(context_wrap(SCSI_HOSTS_2, SCSI_HOST2_PATH))}
    failed, total = doctest.testmod(scsi_eh_deadline, globs=env)
    assert failed == 0