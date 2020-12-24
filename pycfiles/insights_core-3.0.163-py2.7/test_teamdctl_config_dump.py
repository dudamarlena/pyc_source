# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_teamdctl_config_dump.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.teamdctl_config_dump import TeamdctlConfigDump
from insights.parsers import teamdctl_config_dump
from insights.tests import context_wrap
import doctest
TEAMDCTL_CONFIG_DUMP_INFO = ('\n{\n    "device": "team0",\n    "hwaddr": "DE:5D:21:A8:98:4A",\n    "link_watch": [\n        {\n            "delay_up": 5,\n            "name": "ethtool"\n        },\n        {\n            "name": "nsna_ping",\n            "target_host ": "target.host"\n        }\n    ],\n    "mcast_rejoin": {\n        "count": 1\n    },\n    "notify_peers": {\n        "count": 1\n    },\n    "runner": {\n        "hwaddr_policy": "only_active",\n        "name": "activebackup"\n    }\n}\n').strip()

def test_teamdctl_state_dump():
    result = TeamdctlConfigDump(context_wrap(TEAMDCTL_CONFIG_DUMP_INFO))
    assert result.device_name == 'team0'
    assert result.runner_name == 'activebackup'
    assert result.runner_hwaddr_policy == 'only_active'


def test_nmcli_doc_examples():
    env = {'teamdctl_config_dump': TeamdctlConfigDump(context_wrap(TEAMDCTL_CONFIG_DUMP_INFO))}
    failed, total = doctest.testmod(teamdctl_config_dump, globs=env)
    assert failed == 0