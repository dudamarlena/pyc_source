# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_scheduler.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import scheduler
from insights.tests import context_wrap
SDA_SCHEDULER = ('\nnoop deadline [cfq]\n').strip()
SDB_SCHEDULER = ('\nnoop [deadline] cfq\n').strip()
VDC_SCHEDULER = ('\n[noop] deadline cfq\n').strip()
SDA_PATH = '/sys/block/sda/queue/scheduler'
SDB_PATH = '/sys/block/sdb/queue/scheduler'
VDC_PATH = '/sys/block/vdc/queue/scheduler'

def test_scheduler_cfq():
    r = scheduler.Scheduler(context_wrap(SDA_SCHEDULER, SDA_PATH))
    assert r.data['sda'] == '[cfq]'


def test_scheduler_deadline():
    r = scheduler.Scheduler(context_wrap(SDB_SCHEDULER, SDB_PATH))
    assert r.data['sdb'] == '[deadline]'


def test_scheduler_noop():
    r = scheduler.Scheduler(context_wrap(VDC_SCHEDULER, VDC_PATH))
    assert r.data['vdc'] == '[noop]'