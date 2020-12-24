# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_passenger_status.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers import SkipException
from insights.parsers import passenger_status
from insights.parsers.passenger_status import PassengerStatus
from insights.tests import context_wrap
import pytest, doctest
PASS_STATUS = '\nVersion : 4.0.18\nDate    : 2018-10-23 15:42:04 +0800\nInstance: 1265\n----------- General information -----------\nMax pool size : 12\nProcesses     : 2\nRequests in top-level queue : 0\n\n----------- Application groups -----------\n/usr/share/foreman#default:\n  App root: /usr/share/foreman\n  Requests in queue: 192\n  * PID: 30131   Sessions: 1       Processed: 991     Uptime: 2h 9m 8s\n    CPU: 3%      Memory  : 562M    Last used: 1h 53m 51s\n  * PID: 32450   Sessions: 1       Processed: 966     Uptime: 2h 8m 15s\n    CPU: 4%      Memory  : 463M    Last used: 1h 48m 17\n  * PID: 4693    Sessions: 1       Processed: 939     Uptime: 2h 6m 32s\n    CPU: 3%      Memory  : 470M    Last used: 1h 50m 48\n\n/etc/puppet/rack#default:\n  App root: /etc/puppet/rack\n  Requests in queue: 0\n  * PID: 21934   Sessions: 1       Processed: 380     Uptime: 1h 33m 34s\n    CPU: 1%      Memory  : 528M    Last used: 1h 29m 4\n  * PID: 26194   Sessions: 1       Processed: 544     Uptime: 1h 31m 34s\n    CPU: 2%      Memory  : 490M    Last used: 1h 23m 5\n  * PID: 32384   Sessions: 1       Processed: 36      Uptime: 1h 0m 29s\n    CPU: 0%      Memory  : 561M    Last used: 1h 0m 3s\n'
PASS_STATUS_SP = '\nVersion : 4.0.18\nDate    : 2019-06-10 03:17:38 +0100\nInstance: 14745\n----------- General information -----------\nMax pool size : 60\nProcesses     : 7\nRequests in top-level queue : 0\n\n----------- Application groups -----------\n/usr/share/foreman#default:\n  App root: /usr/share/foreman\n  Requests in queue: 0\n  * PID: 39176  Sessions: 0     Processed: 194     Uptime: 24h 9m 0s\n    CPU: 0%     Memory  : 488M  Last used: 20m 24s a\n  * PID: 39342  Sessions: 0       Processed: 0       Uptime: 24h 8m 58s\n    CPU: 0%     Memory  : 178M    Last used: 24h 8m 5\n  * PID: 39377  Sessions: 0       Processed: 0       Uptime: 24h 8m 58s\n    CPU: 0%     Memory  : 179M    Last used: 24h 8m 5\n  * PID: 39478  Sessions: 0       Processed: 0       Uptime: 24h 8m 57s\n    CPU: 0%     Memory  : 178M    Last used: 24h 8m 5\n  * PID: 39525  Sessions: 0       Processed: 0       Uptime: 24h 8m 57s\n    CPU: 0%     Memory  : 173M    Last used: 24h 8m 5\n  * PID: 39614  Sessions: 0       Processed: 0       Uptime: 24h 8m 56s\n    CPU: 0%     Memory  : 174M    Last used: 24h 8m 5\n\n/etc/puppet/rack#default:\n  App root: /etc/puppet/rack\n  Requests in queue: 0\n  * PID: 39667   Sessions: 0       Processed: 241     Uptime: 24h 8m 56s\n    CPU: 0%      Memory  : 45M     Last used: 20m 24s\n'
PASS_STATUS_EXP1 = '\nwrong content\n'

def test_passenger_status():
    passenger_status = PassengerStatus(context_wrap(PASS_STATUS))
    assert passenger_status['Version'] == '4.0.18'
    assert len(passenger_status['foreman_default']['p_list']) == 3
    assert 'rack_default' in passenger_status


def test_passenger_status_2():
    passenger_status = PassengerStatus(context_wrap(PASS_STATUS_SP))
    assert passenger_status['Version'] == '4.0.18'
    assert len(passenger_status['foreman_default']['p_list']) == 6
    foreman_default_p_list = passenger_status['foreman_default']['p_list']
    assert foreman_default_p_list[0] == {'PID': '39176', 
       'Sessions': '0', 'Processed': '194', 'Uptime': '24h 9m 0s', 'CPU': '0%', 
       'Memory': '488M', 'Last used': '20m 24s a'}
    assert foreman_default_p_list[1] == {'PID': '39342', 
       'Sessions': '0', 'Processed': '0', 'Uptime': '24h 8m 58s', 'CPU': '0%', 
       'Memory': '178M', 'Last used': '24h 8m 5'}
    assert foreman_default_p_list[(-1)] == {'PID': '39614', 
       'Sessions': '0', 'Processed': '0', 'Uptime': '24h 8m 56s', 'CPU': '0%', 
       'Memory': '174M', 'Last used': '24h 8m 5'}
    assert 'rack_default' in passenger_status


def test_passenger_status_ex():
    with pytest.raises(SkipException):
        PassengerStatus(context_wrap(PASS_STATUS_EXP1))


def test_passenger_status_doc_examples():
    env = {'passenger_status': PassengerStatus(context_wrap(PASS_STATUS))}
    failed, total = doctest.testmod(passenger_status, globs=env)
    assert failed == 0