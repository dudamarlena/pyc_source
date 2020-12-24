# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_pam.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.parsers.pam import PamConf, PamDConf, PamConfEntry
from insights.parsers import get_active_lines, pam
from insights.tests import context_wrap
import doctest
PAM_CONF_DATA = '\n#%PAM-1.0\nvsftpd      auth        required    pam_securetty.so\nvsftpd      auth        requisite   pam_unix.so nullok\nvsftpd      auth        sufficient  pam_nologin.so\nvsftpd      account     optional    pam_unix.so\nother       password    include     pam_cracklib.so retry=3 logging=verbose\nother       password    required    pam_unix.so shadow nullok use_authtok\nother       session     required    pam_unix.so\n'

def test_pam_conf():
    pam_conf = PamConf(context_wrap(PAM_CONF_DATA))
    assert len(pam_conf) == 7
    assert pam_conf[0].service == 'vsftpd'
    assert pam_conf[0].interface == 'auth'
    assert len(pam_conf[0].control_flags) == 1
    assert pam_conf[0].control_flags[0].flag == 'required'
    assert pam_conf[0].control_flags[0].value is None
    assert pam_conf[0].module_name == 'pam_securetty.so'
    assert pam_conf[0].module_args is None
    assert pam_conf[5].service == 'other'
    assert pam_conf[5].interface == 'password'
    assert len(pam_conf[5].control_flags) == 1
    assert pam_conf[5].control_flags[0].flag == 'required'
    assert pam_conf[5].control_flags[0].value is None
    assert pam_conf[5].module_name == 'pam_unix.so'
    assert pam_conf[5].module_args == 'shadow nullok use_authtok'
    vsftpd = list(pam_conf.search(service='vsftpd'))
    assert len(vsftpd) == 4
    assert vsftpd[0] == pam_conf[0]
    assert vsftpd[1] == pam_conf[1]
    assert vsftpd[2] == pam_conf[2]
    assert vsftpd[3] == pam_conf[3]
    vsftpd_acct = list(pam_conf.search(service='vsftpd', interface='account'))
    assert len(vsftpd_acct) == 1
    assert vsftpd_acct[0] == pam_conf[3]
    assert repr(pam_conf[0]) == '<PamConfEntry for vsftpd: auth required pam_securetty.so>'
    assert repr(pam_conf[4]) == '<PamConfEntry for other: password include pam_cracklib.so retry=3 logging=verbose>'
    return


PAMD_CONF_SSHD_DOCS = '\n#%PAM-1.0\nauth       required     pam_sepermit.so\nauth       substack     password-auth\nauth       include      postlogin\n# Used with polkit to reauthorize users in remote sessions\n-auth      optional     pam_reauthorize.so prepare\naccount    required     pam_nologin.so\naccount    include      password-auth\npassword   include      password-auth\n# pam_selinux.so close should be the first session rule\nsession    required     pam_selinux.so close\nsession    required     pam_loginuid.so\n# pam_selinux.so open should only be followed by sessions to be executed in the user context\nsession    required     pam_selinux.so open env_params\nsession    required     pam_namespace.so\nsession    optional     pam_keyinit.so force revoke\nsession    include      password-auth\nsession    include      postlogin\n# Used with polkit to reauthorize users in remote sessions\n-session   optional     pam_reauthorize.so prepare\n'
PAMD_CONF_DATA = '\n#%PAM-1.0\nauth        required    pam_securetty.so\nauth        requisite   pam_unix.so nullok\nauth        sufficient  pam_nologin.so\nauth        [success=2 default=ok]  pam_debug.so auth=perm_denied cred=success\naccount     optional    pam_unix.so\npassword    include     pam_cracklib.so retry=3 logging=verbose\npassword    required    pam_unix.so shadow nullok use_authtok\nauth        required    pam_listfile.so                    onerr=succeed item=user sense=deny file=/etc/ftpusers\nsession     required    pam_unix.so\n'

def test_pamd_conf():
    pamd_conf = PamDConf(context_wrap(PAMD_CONF_DATA, path='etc/pamd.d/vsftpd'))
    assert len(pamd_conf) == 9
    assert pamd_conf[0].service == 'vsftpd'
    assert pamd_conf[0].interface == 'auth'
    assert len(pamd_conf[0].control_flags) == 1
    assert pamd_conf[0].control_flags[0].flag == 'required'
    assert pamd_conf[0].control_flags[0].value is None
    assert pamd_conf[0].module_name == 'pam_securetty.so'
    assert pamd_conf[0].module_args is None
    assert len(pamd_conf[3].control_flags) == 2
    assert pamd_conf[3].control_flags == [
     PamConfEntry.ControlFlag(flag='success', value='2'),
     PamConfEntry.ControlFlag(flag='default', value='ok')]
    assert pamd_conf[7].interface == 'auth'
    assert len(pamd_conf[7].control_flags) == 1
    assert pamd_conf[7].control_flags[0].flag == 'required'
    assert pamd_conf[7].control_flags[0].value is None
    assert pamd_conf[7].module_name == 'pam_listfile.so'
    assert pamd_conf[7].module_args == 'onerr=succeed item=user sense=deny file=/etc/ftpusers'
    assert pamd_conf[7].module_args_dict == {'onerr': 'succeed', 
       'item': 'user', 'sense': 'deny', 'file': '/etc/ftpusers'}
    default_set = pamd_conf.search(control_flags__contains='default')
    assert len(default_set) == 1
    assert default_set[0] == pamd_conf[3]
    verbose_set = pamd_conf.search(module_args__contains='verbose')
    assert len(verbose_set) == 1
    assert verbose_set[0] == pamd_conf[5]
    return


PAMD_MISC = '\n# Miscellaneous trickier lines\npassword  required pam_cracklib.so                        difok=3 minlen=15 dcredit= 2 ocredit=2\nauth    requisite       pam_permit.so\nauth    [success=2 default=ok]  pam_debug.so auth=perm_denied cred=success\npassword optional pam_exec.so seteuid /usr/bin/make -C /var/yp\n-session optional pam_no_module.so ignore if module not found\n'

def test_pamd_misc_conf():
    misc = PamDConf(context_wrap(PAMD_MISC, path='etc/pamd.d/misc'))
    assert misc
    assert len(misc) == 5
    assert misc[0].service == 'misc'
    assert misc[0].interface == 'password'
    assert len(misc[0].control_flags) == 1
    assert misc[0].control_flags[0].flag == 'required'
    assert misc[0].control_flags[0].value is None
    assert misc[0].module_name == 'pam_cracklib.so'
    assert misc[0].module_args == 'difok=3 minlen=15 dcredit= 2 ocredit=2'
    assert misc[1].service == 'misc'
    assert misc[1].interface == 'auth'
    assert len(misc[1].control_flags) == 1
    assert misc[1].control_flags[0].flag == 'requisite'
    assert misc[1].control_flags[0].value is None
    assert misc[1].module_name == 'pam_permit.so'
    assert misc[1].module_args is None
    assert misc[2].service == 'misc'
    assert misc[2].interface == 'auth'
    assert len(misc[2].control_flags) == 2
    assert misc[2].control_flags[0].flag == 'success'
    assert misc[2].control_flags[0].value == '2'
    assert misc[2].control_flags[1].flag == 'default'
    assert misc[2].control_flags[1].value == 'ok'
    assert misc[2].module_name == 'pam_debug.so'
    assert misc[2].module_args == 'auth=perm_denied cred=success'
    assert misc[3].service == 'misc'
    assert misc[3].interface == 'password'
    assert len(misc[3].control_flags) == 1
    assert misc[3].control_flags[0].flag == 'optional'
    assert misc[3].control_flags[0].value is None
    assert misc[3].module_name == 'pam_exec.so'
    assert misc[3].module_args == 'seteuid /usr/bin/make -C /var/yp'
    assert misc[4].service == 'misc'
    assert misc[4]._type_raw == '-session'
    assert misc[4].ignored_if_module_not_found
    assert misc[4].interface == 'session'
    assert len(misc[4].control_flags) == 1
    assert misc[4].control_flags[0].flag == 'optional'
    assert misc[4].control_flags[0].value is None
    assert misc[4].module_name == 'pam_no_module.so'
    assert misc[4].module_args == 'ignore if module not found'
    return


PAMD_CONF_DATA_BAD_LINES = '\n#%PAM-1.0\nunrecognised_type\nauth\nauth badcontrol\nauth [success=2 default] no_equals_in_group\nauth required\n'

def test_bad_pamd_files():
    pamd_conf = PamDConf(context_wrap(PAMD_CONF_DATA_BAD_LINES, path='etc/pamd.d/bad'))
    assert pamd_conf
    assert len(pamd_conf) == 5
    for entry in pamd_conf:
        assert entry.service == 'bad'
        assert entry.interface is None
        assert entry.control_flags == []
        assert entry.module_name is None
        assert entry.module_args is None
        assert entry._errors == [("Cannot parse line '{f}' as a valid pam.d entry").format(f=entry._full_line)]

    return


class PamDConfNoService(PamDConf):

    def parse_content(self, content):
        self.data = []
        for line in get_active_lines(content):
            self.data.append(PamConfEntry(line, pamd_conf=True))


def test_bad_pamd_subclass():
    with pytest.raises(ValueError) as (exc):
        pamd_conf = PamDConfNoService(context_wrap(PAMD_CONF_DATA))
        assert pamd_conf is None
    assert 'Service name must be provided for pam.d conf file' in str(exc)
    return


def test_pam_doc_examples():
    env = {'PamDConf': PamDConf, 
       'PamConfEntry': PamConfEntry, 
       'pam_conf': PamConf(context_wrap(PAM_CONF_DATA, path='/etc/pam.conf')), 
       'pamd_conf': PamDConf(context_wrap(PAMD_CONF_SSHD_DOCS, path='/etc/pam.d/sshd'))}
    failed, total = doctest.testmod(pam, globs=env)
    assert failed == 0