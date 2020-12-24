# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_journald_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.journald_conf import JournaldConf
from insights.tests import context_wrap
JOURNALD_CONF_1 = ('\n#  This file is part of systemd.\n#\n#  systemd is free software; you can redistribute it and/or modify it\n#  under the terms of the GNU Lesser General Public License as published by\n#  the Free Software Foundation; either version 2.1 of the License, or\n#  (at your option) any later version.\n#\n# Entries in this file show the compile time defaults.\n# You can change settings by editing this file.\n# Defaults can be restored by simply deleting this file.\n#\n# See journald.conf(5) for details.\n\n[Journal]\n#Storage=auto\nStorage=persistent\n#Compress=yes\n#Seal=yes\nSeal=no\n#SplitMode=uid\n#SyncIntervalSec=5m\n#RateLimitInterval=30s\n#RateLimitBurst=1000\n#SystemMaxUse=\n#SystemKeepFree=\n#SystemMaxFileSize=\n#RuntimeMaxUse=\n#RuntimeKeepFree=\n#RuntimeMaxFileSize=\n#MaxRetentionSec=\n#MaxFileSec=1month\n#ForwardToSyslog=yes\nForwardToSyslog=no\n#ForwardToKMsg=no\n#ForwardToConsole=no\n#ForwardToWall=yes\n#TTYPath=/dev/console\n#MaxLevelStore=debug\n#MaxLevelSyslog=debug\n#MaxLevelKMsg=notice\n#MaxLevelConsole=info\n#MaxLevelWall=emerg\n\n').strip()
JOURNALD_CONF_2 = ('\n#comment\n# comment\n# comment = comment\n# comment = comment = comment\n#comment=comment\n#comment=comment=comment\noption_a=value_a\noption_b = value_b\noption_c= value_c\noption_d =value_d\nbroken_option_e = value_e = value_2_e\nbroken_option_f=value_f=value_2_f\nbroken_option_g\noption_h = value_h # some comment\noption_i = value_i # this must be accessible, even after all these errors\n').strip()
AUDITD_CONF_PATH = '/etc/audit/auditd.conf'

def test_constructor():
    context = context_wrap(JOURNALD_CONF_1, AUDITD_CONF_PATH)
    result = JournaldConf(context)
    assert 'Storage=persistent' in result.active_lines_unparsed
    assert 'no' == result.active_settings['Seal']
    assert '#TTYPath' not in result.active_settings
    assert 'no' == result.get_active_setting_value('ForwardToSyslog')
    context = context_wrap(JOURNALD_CONF_2, AUDITD_CONF_PATH)
    result = JournaldConf(context)
    assert 'comment' not in result.active_settings
    assert 'broken_option_g' not in result.active_settings
    assert 'value_i' == result.get_active_setting_value('option_i')


def test_active_lines_unparsed():
    context = context_wrap(JOURNALD_CONF_1, AUDITD_CONF_PATH)
    result = JournaldConf(context)
    test_active_lines = []
    for line in JOURNALD_CONF_1.split('\n'):
        if not line.strip().startswith('#'):
            if line.strip():
                test_active_lines.append(line)

    assert test_active_lines == result.active_lines_unparsed


def build_active_settings_expected():
    active_settings = {}
    for line in JOURNALD_CONF_1.split('\n'):
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
    context = context_wrap(JOURNALD_CONF_1, AUDITD_CONF_PATH)
    result = JournaldConf(context)
    active_settings = build_active_settings_expected()
    assert active_settings == result.active_settings


def test_get_active_setting_value():
    context = context_wrap(JOURNALD_CONF_1, AUDITD_CONF_PATH)
    result = JournaldConf(context)
    active_settings = build_active_settings_expected()
    for key, value in active_settings.items():
        assert result.get_active_setting_value(key) == value