# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_iscsiadm_mode_session.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.iscsiadm_mode_session import IscsiAdmModeSession
from insights.tests import context_wrap
ISCSIADM_SESSION_INFO = ('\ntcp: [1] 10.72.32.45:3260,1 iqn.2017-06.com.example:server1 (non-flash)\ntcp: [2] 10.72.32.45:3260,1 iqn.2017-06.com.example:server2 (non-flash)\n').strip()
EXPECTED_RESULTS = [
 {'IFACE_TRANSPORT': 'tcp', 'SID': '1', 
    'TARGET_IP': '10.72.32.45:3260,1', 
    'TARGET_IQN': 'iqn.2017-06.com.example:server1'},
 {'IFACE_TRANSPORT': 'tcp', 'SID': '2', 
    'TARGET_IP': '10.72.32.45:3260,1', 
    'TARGET_IQN': 'iqn.2017-06.com.example:server2'}]

def test_iscsiadm_session_info():
    iscsiadm_session_info = IscsiAdmModeSession(context_wrap(ISCSIADM_SESSION_INFO))
    assert iscsiadm_session_info.data == EXPECTED_RESULTS
    assert len(iscsiadm_session_info.data) == 2
    assert iscsiadm_session_info[0] == {'IFACE_TRANSPORT': 'tcp', 
       'SID': '1', 
       'TARGET_IP': '10.72.32.45:3260,1', 
       'TARGET_IQN': 'iqn.2017-06.com.example:server1'}
    assert iscsiadm_session_info[1]['TARGET_IQN'] == 'iqn.2017-06.com.example:server2'