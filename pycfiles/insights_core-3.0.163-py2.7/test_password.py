# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_password.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.password import PasswordAuthPam
from insights.parsers.pam import PamConfEntry
from insights.tests import context_wrap
PW_AUTH_PAM_CONF = ('\n#%PAM-1.0\n# This file is auto-generated.\n# User changes will be destroyed the next time authconfig is run.\nauth        required      pam_env.so\nauth        sufficient    pam_unix.so nullok try_first_pass\nauth        requisite     pam_succeed_if.so uid >= 500 quiet\nauth        required      pam_deny.so\nauth        [default=die] pam_faillock.so authfail deny=3 unlock_time=604800 fail_interval=900\nauth        required      pam_faillock.so authsucc deny=3 unlock_time=604800 fail_interval=900\n\naccount     required      pam_unix.so\naccount     sufficient    pam_localuser.so\naccount     sufficient    pam_succeed_if.so uid < 500 quiet\naccount     required      pam_permit.so\n\npassword    requisite     pam_cracklib.so try_first_pass retry=3 lcredit=-1 ucredit=-1 dcredit=-1 ocredit=-1 minlen=12\npassword    sufficient    pam_unix.so sha512 shadow nullok try_first_pass use_authtok\npassword    required      pam_deny.so\n\nsession     optional      pam_keyinit.so revoke\nsession     required      pam_limits.so\nsession     [success=1 default=ignore] pam_succeed_if.so service in crond quiet use_uid\nsession     required      pam_unix.so\n').strip()

def test_password_auth_pam_conf():
    pam_conf = PasswordAuthPam(context_wrap(PW_AUTH_PAM_CONF, path='etc/pam.d/password-auth'))
    assert len(pam_conf) == 17
    assert pam_conf[0].service == 'password-auth'
    assert pam_conf[0].interface == 'auth'
    assert len(pam_conf[0].control_flags) == 1
    assert pam_conf[0].control_flags[0].flag == 'required'
    assert pam_conf[0].module_name == 'pam_env.so'
    assert pam_conf[0].module_args is None
    assert pam_conf[15].interface == 'session'
    assert len(pam_conf[15].control_flags) == 2
    assert pam_conf[15].control_flags == [PamConfEntry.ControlFlag(flag='success', value='1'),
     PamConfEntry.ControlFlag(flag='default', value='ignore')]
    assert pam_conf[15].module_name == 'pam_succeed_if.so'
    assert pam_conf[15].module_args == 'service in crond quiet use_uid'
    return