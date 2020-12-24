# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ipaupgrade_log.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.ipaupgrade_log import IpaupgradeLog
from insights.tests import context_wrap
from datetime import datetime
IPAUPGRADE_LOG = '\n2017-08-07T07:36:50Z DEBUG Starting external process\n2017-08-07T07:36:50Z DEBUG args=/bin/systemctl is-active pki-tomcatd@pki-tomcat.service\n2017-08-07T07:36:50Z DEBUG Process finished, return code=0\n2017-08-07T07:36:50Z DEBUG stdout=active\n2017-08-07T07:41:50Z ERROR IPA server upgrade failed: Inspect /var/log/ipaupgrade.log and run command ipa-server-upgrade manually.\n'

def test_ipaupgrade_log():
    log = IpaupgradeLog(context_wrap(IPAUPGRADE_LOG))
    assert len(log.get('DEBUG')) == 4
    assert len(list(log.get_after(datetime(2017, 8, 7, 7, 37, 30)))) == 1