# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_neutron_metadata_agent_log.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import neutron_metadata_agent_log
from insights.parsers.neutron_metadata_agent_log import NeutronMetadataAgentLog
from insights.tests import context_wrap
from datetime import datetime
METADATA_AGENT_LOG = ('\n2018-06-08 17:29:55.894 11770 WARNING neutron.agent.metadata.agent [-] Server does not support metadata RPC, fallback to using neutron client\n2018-06-08 17:29:55.907 11770 ERROR neutron.agent.metadata.agent [-] Unexpected error.\n2018-06-08 17:29:56.126 11770 TRACE neutron.agent.metadata.agent Traceback (most recent call last):\n2018-06-08 17:29:56.126 11770 TRACE neutron.agent.metadata.agent   File "/usr/lib/python2.7/site-packages/neutron/agent/metadata/agent.py", line 109, in __call__\n2018-06-08 17:29:56.126 11770 TRACE neutron.agent.metadata.agent     self._authenticate_keystone()\n2018-06-08 17:29:56.126 11770 TRACE neutron.agent.metadata.agent   File "/usr/lib/python2.7/site-packages/neutronclient/client.py", line 218, in _authenticate_keystone\n2018-06-08 17:29:56.126 11770 TRACE neutron.agent.metadata.agent     raise exceptions.Unauthorized(message=resp_body)\n2018-06-08 17:29:56.126 11770 TRACE neutron.agent.metadata.agent Unauthorized: {"error": {"message": "The resource could not be found.", "code": 404, "title": "Not Found"}}\n').strip()

def test_neutron_metadata_agent_log():
    nmda_log = NeutronMetadataAgentLog(context_wrap(METADATA_AGENT_LOG))
    assert len(nmda_log.get('Server does not support metadata RPC, fallback to using neutron client')) == 1
    assert len(list(nmda_log.get_after(datetime(2018, 6, 8, 17, 29, 56)))) == 6
    assert len(nmda_log.get('TRACE')) == 6
    assert 'The resource could not be found' in nmda_log


def test_doc():
    env = {'metadata_agent_log': NeutronMetadataAgentLog(context_wrap(METADATA_AGENT_LOG, path='/var/log/neutron/metadata-agent.log'))}
    failed, total = doctest.testmod(neutron_metadata_agent_log, globs=env)
    assert failed == 0