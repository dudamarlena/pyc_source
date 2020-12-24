# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_openvswitch_logs.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers import openvswitch_logs
from insights.tests import context_wrap
from datetime import datetime
LOG_LINES = '\n2017-03-12T11:56:54.989Z|00001|vlog|INFO|opened log file /var/log/openvswitch/ovsdb-server.log\n2017-03-12T11:56:55.053Z|00002|ovsdb_server|INFO|ovsdb-server (Open vSwitch) 2.4.0\n2017-03-12T11:57:04.988Z|00003|memory|INFO|2664 kB peak resident set size after 10.0 seconds\n2017-03-12T11:57:04.988Z|00004|memory|INFO|cells:816 monitors:1 sessions:2\n2017-03-13T07:41:01.524Z|00005|vlog|INFO|closing log file\n2017-03-13T07:41:02.524Z|00005|testing|INFO|testing handing of messages with | in them\n2017-03-13T07:41:03.524Z|testing messages with not enough fields in them.\n'

def test_ovsdb_server():
    logs = openvswitch_logs.OVSDB_Server_Log(context_wrap(LOG_LINES))
    assert len(logs) == 7
    vlogs = logs.get('vlog')
    assert len(vlogs) == 2
    assert vlogs[0] == {'raw_message': '2017-03-12T11:56:54.989Z|00001|vlog|INFO|opened log file /var/log/openvswitch/ovsdb-server.log', 
       'timestamp': '2017-03-12T11:56:54.989Z', 
       'sequence': '00001', 
       'module': 'vlog', 
       'level': 'INFO', 
       'message': 'opened log file /var/log/openvswitch/ovsdb-server.log'}
    assert vlogs[1] == {'raw_message': '2017-03-13T07:41:01.524Z|00005|vlog|INFO|closing log file', 
       'timestamp': '2017-03-13T07:41:01.524Z', 
       'sequence': '00005', 
       'module': 'vlog', 
       'level': 'INFO', 
       'message': 'closing log file'}
    assert len(list(logs.get_after(datetime(2017, 3, 13, 0, 0, 0)))) == 3
    test_logs = logs.get('testing')
    assert test_logs[0] == {'raw_message': '2017-03-13T07:41:02.524Z|00005|testing|INFO|testing handing of messages with | in them', 
       'timestamp': '2017-03-13T07:41:02.524Z', 
       'sequence': '00005', 
       'module': 'testing', 
       'level': 'INFO', 
       'message': 'testing handing of messages with | in them'}
    assert test_logs[1] == {'raw_message': '2017-03-13T07:41:03.524Z|testing messages with not enough fields in them.'}
    assert len(list(logs.get_after(datetime(2017, 3, 12, 11, 20, 0), 'testing'))) == 2


def test_ovs_vswitch():
    logs = openvswitch_logs.OVS_VSwitchd_Log(context_wrap(LOG_LINES))
    assert len(logs) == 7
    vlogs = logs.get('vlog')
    assert len(vlogs) == 2
    assert vlogs[0] == {'raw_message': '2017-03-12T11:56:54.989Z|00001|vlog|INFO|opened log file /var/log/openvswitch/ovsdb-server.log', 
       'timestamp': '2017-03-12T11:56:54.989Z', 
       'sequence': '00001', 
       'module': 'vlog', 
       'level': 'INFO', 
       'message': 'opened log file /var/log/openvswitch/ovsdb-server.log'}
    assert vlogs[1] == {'raw_message': '2017-03-13T07:41:01.524Z|00005|vlog|INFO|closing log file', 
       'timestamp': '2017-03-13T07:41:01.524Z', 
       'sequence': '00005', 
       'module': 'vlog', 
       'level': 'INFO', 
       'message': 'closing log file'}
    assert len(list(logs.get_after(datetime(2017, 3, 13, 0, 0, 0)))) == 3
    assert len(list(logs.get_after(datetime(2017, 3, 12, 11, 20, 0), 'testing'))) == 2