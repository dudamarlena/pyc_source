# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_vsftpd.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.vsftpd import VsftpdConf, VsftpdPamConf
from insights.tests import context_wrap
VSFTPD_PAM_CONF = ('\n#%PAM-1.0\nsession    optional     pam_keyinit.so    force revoke\nauth       required     pam_listfile.so item=user sense=deny file=/etc/vsftpd/ftpusers onerr=succeed\nauth       required     pam_shells.so\nauth       include      password-auth\naccount    include      password-auth\nsession    required     pam_loginuid.so\nsession    include      password-auth\n').strip()
VSFTPD_CONF = ('\n# No anonymous login\nanonymous_enable=NO\n# Let local users login\nlocal_enable=YES\n\n# Write permissions\nwrite_enable=YES\n# Commented_option=not_present\n').strip()

def test_vsftpd_pam_conf():
    pam_conf = VsftpdPamConf(context_wrap(VSFTPD_PAM_CONF, path='etc/pamd.d/vsftpd'))
    assert len(pam_conf) == 7
    assert pam_conf[0].service == 'vsftpd'
    assert pam_conf[0].interface == 'session'
    assert len(pam_conf[0].control_flags) == 1
    assert pam_conf[0].control_flags[0].flag == 'optional'
    assert pam_conf[0].module_name == 'pam_keyinit.so'
    assert pam_conf[0].module_args == 'force revoke'
    assert pam_conf[1].module_args == 'item=user sense=deny file=/etc/vsftpd/ftpusers onerr=succeed'
    assert pam_conf[6].interface == 'session'
    assert len(pam_conf[6].control_flags) == 1
    assert pam_conf[6].control_flags[0].flag == 'include'
    assert pam_conf[6].module_name == 'password-auth'
    assert pam_conf[6].module_args is None
    return


def test_vsftpd_conf():
    vsftpd_conf = VsftpdConf(context_wrap(VSFTPD_CONF))
    assert vsftpd_conf.get('anonymous_enable') == 'NO'
    assert vsftpd_conf.get('local_enable') == 'YES'
    assert vsftpd_conf.get('write_enable') == 'YES'
    assert 'Commented_option' not in vsftpd_conf