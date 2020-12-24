# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_virt_uuid_facts.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import virt_uuid_facts
from insights.parsers.virt_uuid_facts import VirtUuidFacts
from insights.tests import context_wrap
VIRT_UUID_FACTS = ('\n{"virt.uuid": "4546B285-6C41-5D6R-86G5-0BFR4B3625FS", "uname.machine": "x86"}\n').strip()

def test_virt_uuid_facts():
    result = VirtUuidFacts(context_wrap(VIRT_UUID_FACTS))
    assert result.data == {'virt.uuid': '4546B285-6C41-5D6R-86G5-0BFR4B3625FS', 
       'uname.machine': 'x86'}
    assert result.data['virt.uuid'] == '4546B285-6C41-5D6R-86G5-0BFR4B3625FS'


def test_virt_uuid_facts_doc_examples():
    env = {'VirtUuidFacts': VirtUuidFacts, 
       'virt_uuid_facts': VirtUuidFacts(context_wrap(VIRT_UUID_FACTS))}
    failed, total = doctest.testmod(virt_uuid_facts, globs=env)
    assert failed == 0