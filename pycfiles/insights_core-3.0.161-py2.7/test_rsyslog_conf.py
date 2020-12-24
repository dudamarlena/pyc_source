# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rsyslog_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.rsyslog_conf import RsyslogConf
RSYSLOG_CONF_0 = ('\n:fromhost-ip, regex, "10.0.0.[0-9]" /tmp/my_syslog.log\n$ModLoad imtcp\n$InputTCPServerRun 10514\n$template SpiceTmpl,"%TIMESTAMP%.%TIMESTAMP:::date-subseconds% %syslogtag% %syslogseverity-text%:%msg:::sp-if-no-1st-sp%%msg:::drop-last-lf%\\n"\n$WorkDirectory /var/opt/rsyslog # where to place spool files\n').strip()
RSYSLOG_CONF_1 = ('\n# Provides TCP syslog reception\n#$ModLoad imtcp.so\n#$InputTCPServerRun 514\n:msg, regex, "\\/vob\\/.*\\.[cpp|c|java]" /var/log/appMessages\n').strip()

def test_rsyslog_conf_0():
    ctx = context_wrap(RSYSLOG_CONF_0)
    m = RsyslogConf(ctx)
    d = list(m)
    assert len(m) == 5
    assert len(d) == 5
    assert hasattr(m, 'config_items')
    assert isinstance(m.config_items, dict)
    assert 'ModLoad' in m.config_items
    assert m.config_items['ModLoad'] == 'imtcp'
    assert m.config_items['InputTCPServerRun'] == '10514'
    assert m.config_items['template'] == 'SpiceTmpl,"%TIMESTAMP%.%TIMESTAMP:::date-subseconds% %syslogtag% %syslogseverity-text%:%msg:::sp-if-no-1st-sp%%msg:::drop-last-lf%\\n"'
    assert 'ForwardSyslogHost' not in m.config_items
    assert 'WorkDirectory' in m.config_items
    assert m.config_items['WorkDirectory'] == '/var/opt/rsyslog'
    assert hasattr(m, 'config_val')
    assert m.config_val('ModLoad') == 'imtcp'
    assert m.config_val('ForwardSyslogHost', 'syslog.example.com') == 'syslog.example.com'


def test_rsyslog_conf_1():
    ctx = context_wrap(RSYSLOG_CONF_1)
    m = RsyslogConf(ctx)
    d = list(m)
    assert len(m) == 1
    assert len(d) == 1
    assert 'ModLoad' not in m.config_items
    assert 'InputTCPServerRun' not in m.config_items