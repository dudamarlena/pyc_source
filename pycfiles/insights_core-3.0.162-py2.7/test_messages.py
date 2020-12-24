# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_messages.py
# Compiled at: 2019-05-16 13:41:33
from insights import add_filter
from insights.parsers.messages import Messages
from insights.specs import Specs
from insights.tests import context_wrap
MSGINFO = ('\nMay 18 15:13:34 lxc-rhel68-sat56 jabberd/sm[11057]: session started: jid=rhn-dispatcher-sat@lxc-rhel6-sat56.redhat.com/superclient\nMay 18 15:13:36 lxc-rhel68-sat56 wrapper[11375]: --> Wrapper Started as Daemon\nMay 18 15:13:36 lxc-rhel68-sat56 wrapper[11375]: Launching a JVM...\nMay 18 15:24:28 lxc-rhel68-sat56 yum[11597]: Installed: lynx-2.8.6-27.el6.x86_64\nMay 18 15:36:19 lxc-rhel68-sat56 yum[11954]: Updated: sos-3.2-40.el6.noarch\nApr 22 10:35:01 boy-bona CROND[27921]: (root) CMD (/usr/lib64/sa/sa1 -S DISK 1 1)\nApr 22 10:37:32 boy-bona crontab[28951]: (root) LIST (root)\nApr 22 10:40:01 boy-bona CROND[30677]: (root) CMD (/usr/lib64/sa/sa1 -S DISK 1 1)\nApr 22 10:41:13 boy-bona crontab[32515]: (root) LIST (root)\n').strip()
add_filter(Specs.messages, [
 'LIST',
 'CROND',
 'jabberd',
 'Wrapper',
 'Launching',
 'yum'])

def test_messages():
    msg_info = Messages(context_wrap(MSGINFO))
    bona_list = msg_info.get('(root) LIST (root)')
    assert 2 == len(bona_list)
    assert bona_list[0].get('timestamp') == 'Apr 22 10:37:32'
    assert bona_list[1].get('timestamp') == 'Apr 22 10:41:13'
    crond = msg_info.get('CROND')
    assert 2 == len(crond)
    assert crond[0].get('procname') == 'CROND[27921]'
    assert msg_info.get('jabberd/sm[11057]')[0].get('hostname') == 'lxc-rhel68-sat56'
    assert msg_info.get('Wrapper')[0].get('message') == '--> Wrapper Started as Daemon'
    assert msg_info.get('Launching')[0].get('raw_message') == 'May 18 15:13:36 lxc-rhel68-sat56 wrapper[11375]: Launching a JVM...'
    assert 2 == len(msg_info.get('yum'))