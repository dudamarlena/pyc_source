# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_dirsrv.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import DirsrvSysconfig
from insights.tests import context_wrap
SYSCONFIG = '\n# how many seconds to wait for the startpid file to show\n# up before we assume there is a problem and fail to start\n# if using systemd, omit the "; export VARNAME" at the end\n#STARTPID_TIME=10 ; export STARTPID_TIME\n# how many seconds to wait for the pid file to show\n# up before we assume there is a problem and fail to start\n# if using systemd, omit the "; export VARNAME" at the end\n#PID_TIME=600 ; export PID_TIME\nKRB5CCNAME=/tmp/krb5cc_995\nKRB5_KTNAME=/etc/dirsrv/ds.keytab\n'

def test_dirsrv_sysconfig():
    syscfg = DirsrvSysconfig(context_wrap(SYSCONFIG))
    assert 'PID_TIME' not in syscfg.data
    assert syscfg.data['KRB5CCNAME'] == '/tmp/krb5cc_995'
    assert syscfg.data['KRB5_KTNAME'] == '/etc/dirsrv/ds.keytab'
    assert syscfg['KRB5CCNAME'] == '/tmp/krb5cc_995'
    assert syscfg['KRB5_KTNAME'] == '/etc/dirsrv/ds.keytab'
    assert syscfg.unparsed_lines == []