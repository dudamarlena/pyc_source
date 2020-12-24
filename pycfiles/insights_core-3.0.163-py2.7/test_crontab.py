# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_crontab.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.crontab import CrontabL, HeatCrontab, KeystoneCrontab, NovaCrontab, RootCrontab
from insights.tests import context_wrap
from insights.parsers import ParseException
import pytest
CRONTAB_DATA = '\n# comment line\n* * * * * /usr/bin/keystone-manage token_flush > /dev/null 2>&1\n33 0 1 3 6 /bin/heat-manage purge_deleted -g days 7\n# Test all the range and list and named options\n  00-59/20  1,2,3,5,8,13,21 */2 1,MAR,7-Dec/2   Tue,4-Sun   /bin/mail -s "Foo has occurred" admin%Foo has occurred, time to bail out\n* * * * * user_name /usr/local/bin/motd_update\nMAILTO=admin\nCRON_TZ = Europe/France\n'
CRONTAB_EXTENSIONS = '\n@reboot /usr/local/bin/unmangle_database\n@daily  /usr/sbin/logrotate\n'
CRONTAB_BAD_DATA = '\n* * * *  /usr/bin/heat-manage purge_deleted >/dev/null 2>&1\nError reading crontab\n'
CRONTAB_BAD_NICKNAME = '\n@huorly  /usr/bin/check_init\n'

def crontab_tests(crontab_class):
    crontab = crontab_class(context_wrap(CRONTAB_DATA))
    assert crontab is not None
    assert [ r.get('minute') for r in crontab ] == ['*', '33', '00-59/20', '*']
    assert crontab.search('heat-manage') == [
     {'minute': '33', 'hour': '0', 
        'day_of_month': '1', 
        'month': '3', 
        'day_of_week': '6', 
        'command': '/bin/heat-manage purge_deleted -g days 7'}]
    assert crontab.search('crazy_123') == []
    assert crontab.search('motd')[0]['command'] == 'user_name /usr/local/bin/motd_update'
    assert crontab.invalid_lines == []
    assert hasattr(crontab, 'environment')
    assert isinstance(crontab.environment, dict)
    assert 'MAILTO' in crontab.environment
    assert crontab.environment['MAILTO'] == 'admin'
    assert 'CRON_TZ' in crontab.environment
    assert crontab.environment['CRON_TZ'] == 'Europe/France'
    crontab = crontab_class(context_wrap(CRONTAB_DATA + CRONTAB_BAD_DATA))
    assert crontab is not None
    assert crontab.invalid_lines == [
     '* * * *  /usr/bin/heat-manage purge_deleted >/dev/null 2>&1',
     'Error reading crontab']
    crontab = crontab_class(context_wrap(CRONTAB_EXTENSIONS))
    assert crontab is not None
    assert crontab.invalid_lines == []
    assert crontab[0] == {'time': '@reboot', 
       'command': '/usr/local/bin/unmangle_database'}
    assert crontab[1] == {'minute': '0', 
       'hour': '0', 
       'day_of_month': '*', 
       'month': '*', 
       'day_of_week': '*', 
       'command': '/usr/sbin/logrotate'}
    with pytest.raises(ParseException) as (exc):
        crontab = crontab_class(context_wrap(CRONTAB_EXTENSIONS + CRONTAB_BAD_NICKNAME))
    assert "@huorly not recognised as a time specification 'nickname'" in str(exc)
    crontab = crontab_class(context_wrap(CRONTAB_EXTENSIONS))
    assert crontab is not None
    assert crontab.invalid_lines == []
    assert crontab[0] == {'time': '@reboot', 
       'command': '/usr/local/bin/unmangle_database'}
    assert crontab[1] == {'minute': '0', 
       'hour': '0', 
       'day_of_month': '*', 
       'month': '*', 
       'day_of_week': '*', 
       'command': '/usr/sbin/logrotate'}
    return


def test_crontab():
    crontab_tests(CrontabL)


def test_heat_crontab():
    crontab_tests(HeatCrontab)


def test_keystone_crontab():
    crontab_tests(KeystoneCrontab)


def test_nova_crontab():
    crontab_tests(NovaCrontab)


def test_root_crontab():
    crontab_tests(RootCrontab)