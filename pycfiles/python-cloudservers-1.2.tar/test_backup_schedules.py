# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/cloudservers/tests/test_backup_schedules.py
# Compiled at: 2010-08-16 13:11:38
from cloudservers.backup_schedules import *
from fakeserver import FakeServer
from utils import assert_isinstance
cs = FakeServer()

def test_get_backup_schedule():
    s = cs.servers.get(1234)
    b = cs.backup_schedules.get(server=s)
    assert_isinstance(b, BackupSchedule)
    cs.assert_called('GET', '/servers/1234/backup_schedule')
    b = cs.backup_schedules.get(server=1234)
    assert_isinstance(b, BackupSchedule)
    cs.assert_called('GET', '/servers/1234/backup_schedule')
    assert_isinstance(s.backup_schedule, BackupSchedule)
    cs.assert_called('GET', '/servers/1234/backup_schedule')
    b = s.backup_schedule.get()
    cs.assert_called('GET', '/servers/1234/backup_schedule')


def test_create_update_backup_schedule():
    s = cs.servers.get(1234)
    cs.backup_schedules.update(server=s, enabled=True, weekly=BACKUP_WEEKLY_THURSDAY, daily=BACKUP_DAILY_H_1000_1200)
    cs.assert_called('POST', '/servers/1234/backup_schedule')
    s.backup_schedule.update(enabled=False)
    cs.assert_called('POST', '/servers/1234/backup_schedule')


def test_delete_backup_schedule():
    s = cs.servers.get(1234)
    cs.backup_schedules.delete(s)
    cs.assert_called('DELETE', '/servers/1234/backup_schedule')
    cs.backup_schedules.delete(1234)
    cs.assert_called('DELETE', '/servers/1234/backup_schedule')
    s.backup_schedule.delete()
    cs.assert_called('DELETE', '/servers/1234/backup_schedule')