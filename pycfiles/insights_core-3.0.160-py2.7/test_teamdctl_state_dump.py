# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_teamdctl_state_dump.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.teamdctl_state_dump import TeamdctlStateDump
from insights.tests import context_wrap
TEAMDCTL_STATE_DUMP_INFO = ('\n{\n    "runner": {\n        "active_port": "eno1"\n    },\n    "setup": {\n        "daemonized": false,\n        "dbus_enabled": true,\n        "debug_level": 0,\n        "kernel_team_mode_name": "activebackup",\n        "pid": 4464,\n        "pid_file": "/var/run/teamd/team0.pid",\n        "runner_name": "activebackup",\n        "zmq_enabled": false\n    },\n    "team_device": {\n        "ifinfo": {\n            "dev_addr": "2c:59:e5:47:a9:04",\n            "dev_addr_len": 6,\n            "ifindex": 5,\n            "ifname": "team0"\n        }\n    }\n}\n').strip()
TEAMDCTL_STATE_DUMP_INFO_NONE = ('\n{\n    "runner": {\n    },\n    "setup": {\n        "daemonized": false,\n        "dbus_enabled": true,\n        "debug_level": 0,\n        "kernel_team_mode_name": "activebackup",\n        "pid": 4464,\n        "pid_file": "/var/run/teamd/team0.pid",\n        "runner_name": "activebackup",\n        "zmq_enabled": false\n    },\n    "team_device": {\n        "ifinfo": {\n            "dev_addr": "2c:59:e5:47:a9:04",\n            "dev_addr_len": 6,\n            "ifindex": 5\n        }\n    }\n}\n').strip()

def test_teamdctl_state_dump():
    result = TeamdctlStateDump(context_wrap(TEAMDCTL_STATE_DUMP_INFO))
    assert result.data == {'runner': {'active_port': 'eno1'}, 
       'setup': {'daemonized': False, 
                 'zmq_enabled': False, 
                 'kernel_team_mode_name': 'activebackup', 
                 'pid': 4464, 
                 'dbus_enabled': True, 
                 'debug_level': 0, 
                 'pid_file': '/var/run/teamd/team0.pid', 
                 'runner_name': 'activebackup'}, 
       'team_device': {'ifinfo': {'ifindex': 5, 
                                  'dev_addr': '2c:59:e5:47:a9:04', 
                                  'ifname': 'team0', 
                                  'dev_addr_len': 6}}}
    assert result['runner']['active_port'] == 'eno1'
    assert result['setup']['runner_name'] == 'activebackup'
    assert result.runner_type == 'activebackup'
    assert result.team_ifname == 'team0'


def test_teamdctl_state_dump_none():
    result = TeamdctlStateDump(context_wrap(TEAMDCTL_STATE_DUMP_INFO_NONE))
    assert result.data == {'runner': {}, 'setup': {'daemonized': False, 
                 'zmq_enabled': False, 
                 'kernel_team_mode_name': 'activebackup', 
                 'pid': 4464, 
                 'dbus_enabled': True, 
                 'debug_level': 0, 
                 'pid_file': '/var/run/teamd/team0.pid', 
                 'runner_name': 'activebackup'}, 
       'team_device': {'ifinfo': {'ifindex': 5, 
                                  'dev_addr': '2c:59:e5:47:a9:04', 
                                  'dev_addr_len': 6}}}
    assert result['setup']['runner_name'] == 'activebackup'
    assert result.runner_type == 'activebackup'
    assert result.team_ifname is None
    return