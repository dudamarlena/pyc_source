# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_samba_logs.py
# Compiled at: 2020-03-25 13:10:41
from insights.parsers import samba_logs
from insights.parsers.samba_logs import SAMBALog
from insights.tests import context_wrap
import doctest
SAMBA_LOG_NORMAL = "\n[2019/11/25 19:29:23.933547,  0] ../lib/util/become_daemon.c:138(daemon_ready)  daemon_ready: STATUS=daemon 'smbd' finished starting up and ready to serve connections\n[2019/11/25 19:32:12.511867,  0] ../lib/util/become_daemon.c:138(daemon_ready)  daemon_ready: STATUS=daemon 'smbd' finished starting up and ready to serve connections\n[2019/11/27 11:11:04.900434,  5, pid=15817, effective(0, 0), real(0, 0)] ../source3/lib/messages.c:709(messaging_register)  Registering messaging pointer for type 13 - private_data=(nil)\n[2019/11/27 11:11:04.900450,  5, pid=15817, effective(0, 0), real(0, 0)] ../source3/lib/messages.c:709(messaging_register)  Registering messaging pointer for type 33 - private_data=0x557a635cb3e0\n[2019/11/27 11:11:04.911688, 10, pid=15822, effective(0, 0), real(0, 0)] ../source3/printing/print_cups.c:203(recv_pcap_blob)  successfully recvd blob of len 12\n[2019/11/27 11:11:04.911718,  3, pid=15822, effective(0, 0), real(0, 0)] ../source3/printing/print_cups.c:536(cups_async_callback)  failed to retrieve printer list: NT_STATUS_UNSUCCESSFUL\n[2019/45/899 11:11:04.911718,  3, pid=15822, effective(0, 0), real(0, 0)] Fake line to check that date parsing handles corrupted dates\n[2019/45/899 11:11:04.911891,  3, pid=15822, effective(0, 0), real(0, 0)] ../source3/printing/queue_process.c:236(bq_sig_hup_handler) Reloading pcap cache after SIGHUP.\n"
SAMBALog.keep_scan('sighups', 'SIGHUP')

def test_normal_samba_logs():
    samba_logs = SAMBALog(context_wrap(SAMBA_LOG_NORMAL))
    assert samba_logs is not None
    assert samba_logs.get('messaging_register')[0]['pid'] == 'pid=15817'
    assert samba_logs.get('0x557a635cb3e0')[0]['function'] == '../source3/lib/messages.c:709(messaging_register)'
    assert samba_logs.get('cups_async_callback')[0]['timestamp'] == '2019/11/27 11:11:04.911718'
    assert samba_logs.get('0x557a635cb3e0')[0]['timestamp'] == '2019/11/27 11:11:04.900450'
    assert len(samba_logs.get('Fake line')) == 1
    return


def test_samba_logs_doc():
    env = {'samba_logs': SAMBALog(context_wrap(SAMBA_LOG_NORMAL))}
    failed, total = doctest.testmod(samba_logs, globs=env)
    assert failed == 0