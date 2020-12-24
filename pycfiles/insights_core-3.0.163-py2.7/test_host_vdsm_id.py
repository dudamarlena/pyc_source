# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_host_vdsm_id.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.host_vdsm_id import VDSMId
UUID = 'F7D9D983-6233-45C2-A387-9B0C33CB1306'
UUID_CONTENT = ('\n# VDSM UUID info\n#\nF7D9D983-6233-45C2-A387-9B0C33CB1306\n').strip()

def test_get_vdsm_id():
    expected = VDSMId(context_wrap(UUID_CONTENT))
    assert UUID == expected.uuid