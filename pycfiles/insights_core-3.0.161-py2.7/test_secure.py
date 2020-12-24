# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_secure.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.secure import Secure
from insights.tests import context_wrap
from datetime import datetime
MSGINFO = ('\nAug 24 09:31:39 localhost polkitd[822]: Loading rules from directory /etc/polkit-1/rules.d\nAug 24 09:31:39 localhost polkitd[822]: Loading rules from directory /usr/share/polkit-1/rules.d\nAug 24 09:31:39 localhost polkitd[822]: Finished loading, compiling and executing 6 rules\nAug 24 09:31:39 localhost polkitd[822]: Acquired the name org.freedesktop.PolicyKit1 on the system bus\nAug 25 13:52:54 localhost sshd[23085]: pam_unix(sshd:session): session opened for user zjj by (uid=0)\nAug 25 13:52:54 localhost sshd[23085]: error: openpty: No such file or directory\nAug 25 13:52:54 localhost sshd[23089]: error: session_pty_req: session 0 alloc failed\nAug 25 14:04:04 localhost sshd[23089]: Received disconnect from 10.66.192.100: 11: disconnected by user\nAug 25 14:04:04 localhost sshd[23085]: pam_unix(sshd:session): session closed for user zjj\nStrange line with : but not otherwise parseable for testing code correctness\n    Test continuation line\n').strip()

def test_secure():
    msg_info = Secure(context_wrap(MSGINFO))
    ssh_list = msg_info.get('sshd')
    assert 5 == len(ssh_list)
    assert ssh_list[0].get('timestamp') == 'Aug 25 13:52:54'
    assert ssh_list[4].get('timestamp') == 'Aug 25 14:04:04'
    polkitd = msg_info.get('Loading rules from directory')
    assert 2 == len(polkitd)
    assert polkitd[0].get('procname') == 'polkitd[822]'
    assert polkitd[1].get('raw_message') == 'Aug 24 09:31:39 localhost polkitd[822]: Loading rules from directory /usr/share/polkit-1/rules.d'
    assert polkitd[1].get('message') == 'Loading rules from directory /usr/share/polkit-1/rules.d'
    assert polkitd[1].get('hostname') == 'localhost'
    assert msg_info.get('continuation') == [
     {'raw_message': '    Test continuation line'}]
    assert msg_info.get('Strange line') == [
     {'raw_message': 'Strange line with : but not otherwise parseable for testing code correctness', 
        'message': 'but not otherwise parseable for testing code correctness'}]
    assert len(list(msg_info.get_after(datetime(2017, 8, 25, 0, 0, 0)))) == 7