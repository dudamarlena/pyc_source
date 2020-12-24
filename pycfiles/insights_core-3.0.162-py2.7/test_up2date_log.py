# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_up2date_log.py
# Compiled at: 2019-05-16 13:41:33
from datetime import datetime
from insights.parsers.up2date_log import Up2dateLog
from insights.tests import context_wrap
import doctest
from insights.parsers import up2date_log
LOG1 = ('\n[Thu Feb  1 10:40:13 2018] rhn_register ERROR: can not find RHNS CA file: /usr/share/rhn/RHN-ORG-TRUSTED-SSL-CERT\n[Thu Feb  1 10:40:22 2018] rhn_register ERROR: can not find RHNS CA file: /usr/share/rhn/RHN-ORG-TRUSTED-SSL-CERT\n[Thu Feb  1 10:40:22 2018] rhn_register\nTraceback (most recent call last):\n  File "/usr/sbin/rhn_register", line 74, in <module>\n    app.run()\n  File "/usr/share/rhn/up2date_client/rhncli.py", line 96, in run\n    sys.exit(self.main() or 0)\n  File "/usr/sbin/rhn_register", line 60, in main\n    if not up2dateAuth.getLoginInfo():\n  File "/usr/share/rhn/up2date_client/up2dateAuth.py", line 228, in getLoginInfo\n    login(timeout=timeout)\n  File "/usr/share/rhn/up2date_client/up2dateAuth.py", line 179, in login\n    server = rhnserver.RhnServer(timeout=timeout)\n  File "/usr/share/rhn/up2date_client/rhnserver.py", line 172, in __init__\n    timeout=timeout)\n  File "/usr/share/rhn/up2date_client/rpcServer.py", line 172, in getServer\n    raise up2dateErrors.SSLCertificateFileNotFound(msg)\n<class \'up2date_client.up2dateErrors.SSLCertificateFileNotFound\'>: ERROR: can not find RHNS CA file: /usr/share/rhn/RHN-ORG-TRUSTED-SSL-CERT\n').strip()
LOG2 = "\n[Thu Feb  1 02:46:25 2018] rhn_register updateLoginInfo() login info\n[Thu Feb  1 02:46:35 2018] rhn_register A socket error occurred: (-3, 'Temporary failure in name resolution'), attempt #1\n[Thu Feb  1 02:46:40 2018] rhn_register A socket error occurred: (-3, 'Temporary failure in name resolution'), attempt #2\n[Thu Feb  1 02:46:45 2018] rhn_register A socket error occurred: (-3, 'Temporary failure in name resolution'), attempt #3\n[Thu Feb  1 02:46:50 2018] rhn_register A socket error occurred: (-3, 'Temporary failure in name resolution'), attempt #4\n[Thu Feb  1 02:46:55 2018] rhn_register A socket error occurred: (-3, 'Temporary failure in name resolution'), attempt #5\n"

def test_up2date_log():
    ulog = Up2dateLog(context_wrap(LOG1))
    ern_list = ulog.get('ERROR')
    assert 3 == len(ern_list)
    assert ern_list[2]['raw_message'] == "<class 'up2date_client.up2dateErrors.SSLCertificateFileNotFound'>: ERROR: can not find RHNS CA file: /usr/share/rhn/RHN-ORG-TRUSTED-SSL-CERT"
    assert len(list(ulog.get_after(datetime(2018, 2, 1, 10, 40, 22)))) == 18
    ulog = Up2dateLog(context_wrap(LOG2))
    ern_list = ulog.get('Temporary failure in name resolution')
    assert 5 == len(ern_list)
    assert ern_list[0]['raw_message'] == "[Thu Feb  1 02:46:35 2018] rhn_register A socket error occurred: (-3, 'Temporary failure in name resolution'), attempt #1"
    assert len(list(ulog.get_after(datetime(2018, 2, 1, 2, 46, 45)))) == 3


def test_up2date_log_doc_examples():
    env = {'Up2dateLog': Up2dateLog, 
       'ulog': Up2dateLog(context_wrap(LOG2))}
    failed, total = doctest.testmod(up2date_log, globs=env)
    assert failed == 0