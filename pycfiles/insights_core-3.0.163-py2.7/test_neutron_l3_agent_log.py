# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_neutron_l3_agent_log.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import neutron_l3_agent_log
from insights.parsers.neutron_l3_agent_log import NeutronL3AgentLog
from insights.tests import context_wrap
from datetime import datetime
AGENT_LOG = '\n2017-09-17 10:05:06.241 141544 INFO neutron.agent.l3.ha [-] Router 01d51830-0e3e-4100-a891-efd7dbc000b1 transitioned to backup\n2017-09-17 10:05:07.828 141544 WARNING neutron.agent.linux.iptables_manager [-] Duplicate iptables rule detected. This may indicate a bug in the the iptables rule generation code. Line: -A neutron-l3-agent-INPUT -p tcp -m tcp --dport 9697 -j DROP\n2017-09-17 10:05:07.829 141544 WARNING neutron.agent.linux.iptables_manager [-] Duplicate iptables rule detected. This may indicate a bug in the the iptables rule generation code. Line: -A neutron-l3-agent-INPUT -m mark --mark 0x1/0xffff -j ACCEP\n'

def test_metrics_log():
    log = NeutronL3AgentLog(context_wrap(AGENT_LOG))
    assert len(log.get('INFO')) == 1
    assert 'Duplicate iptables rule detected' in log
    assert len(log.get('Duplicate iptables rule detected')) == 2
    assert len(list(log.get_after(datetime(2017, 2, 17, 19, 36, 38)))) == 3


def test_doc():
    env = {'agent_log': NeutronL3AgentLog(context_wrap(AGENT_LOG, path='/var/log/neutron/l3-agent.log'))}
    failed, total = doctest.testmod(neutron_l3_agent_log, globs=env)
    assert failed == 0