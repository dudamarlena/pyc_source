# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_auditd_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.auditd_conf import AuditdConf
from insights.tests import context_wrap
AUDITD_CONF_1 = ('\n#\n# This file controls the configuration of the audit daemon\n#\n\nlog_file = /var/log/audit/audit.log\nlog_format = RAW\nlog_group = root\npriority_boost = 4\nflush = INCREMENTAL\nfreq = 20\nnum_logs = 5\ndisp_qos = lossy\ndispatcher = /sbin/audispd\nname_format = NONE\n##name = mydomain\nmax_log_file = 6\nmax_log_file_action = ROTATE\nspace_left = 75\nspace_left_action = SYSLOG\naction_mail_acct = root\nadmin_space_left = 50\nadmin_space_left_action = SUSPEND\ndisk_full_action = SUSPEND\ndisk_error_action = SUSPEND\n##tcp_listen_port =\ntcp_listen_queue = 5\ntcp_max_per_addr = 1\n##tcp_client_ports = 1024-65535\ntcp_client_max_idle = 0\nenable_krb5 = no\nkrb5_principal = auditd\n##krb5_key_file = /etc/audit/audit.key\n\n').strip()
AUDITD_CONF_2 = ('\n#comment\n# comment\n# comment = comment\n# comment = comment = comment\n#comment=comment\n#comment=comment=comment\noption_a=value_a\noption_b = value_b\noption_c= value_c\noption_d =value_d\nbroken_option_e = value_e = value_2_e\nbroken_option_f=value_f=value_2_f\nbroken_option_g\noption_h = value_h # some comment\noption_i = value_i # this must be accessible, even after all these errors\n').strip()
AUDITD_CONF_PATH = 'etc/audit/auditd.conf'

def test_constructor():
    context = context_wrap(AUDITD_CONF_1, AUDITD_CONF_PATH)
    result = AuditdConf(context)
    assert 'tcp_listen_queue = 5' in result.active_lines_unparsed
    assert 'SUSPEND' == result.active_settings['disk_error_action']
    assert 'krb5_key_file' not in result.active_settings
    assert '##krb5_key_file' not in result.active_settings
    assert '/var/log/audit/audit.log' == result.get_active_setting_value('log_file')
    context = context_wrap(AUDITD_CONF_2, AUDITD_CONF_PATH)
    result = AuditdConf(context)
    assert 'comment' not in result.active_settings
    assert 'broken_option_g' not in result.active_settings
    assert 'value_i' == result.get_active_setting_value('option_i')


def test_active_lines_unparsed():
    context = context_wrap(AUDITD_CONF_1, AUDITD_CONF_PATH)
    result = AuditdConf(context)
    test_active_lines = []
    for line in AUDITD_CONF_1.split('\n'):
        if not line.strip().startswith('#'):
            if line.strip():
                test_active_lines.append(line)

    assert test_active_lines == result.active_lines_unparsed


def build_active_settings_expected():
    active_settings = {}
    for line in AUDITD_CONF_1.split('\n'):
        if not line.strip().startswith('#'):
            if line.strip():
                try:
                    key, value = line.split('=', 1)
                    key, value = key.strip(), value.strip()
                except:
                    pass
                else:
                    active_settings[key] = value

    return active_settings


def test_active_settings():
    context = context_wrap(AUDITD_CONF_1, AUDITD_CONF_PATH)
    result = AuditdConf(context)
    active_settings = build_active_settings_expected()
    assert active_settings == result.active_settings


def test_get_active_setting_value():
    context = context_wrap(AUDITD_CONF_1, AUDITD_CONF_PATH)
    result = AuditdConf(context)
    active_settings = build_active_settings_expected()
    for key, value in active_settings.items():
        assert result.get_active_setting_value(key) == value