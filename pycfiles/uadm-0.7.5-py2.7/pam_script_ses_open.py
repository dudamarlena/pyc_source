# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uadm/pam_script_ses_open.py
# Compiled at: 2012-07-05 11:59:17
__author__ = 'Pierre-Yves Langlois'
__copyright__ = 'https://github.com/pylanglois/uadm/blob/master/LICENCE'
__credits__ = ['Pierre-Yves Langlois']
__license__ = 'BSD'
__version__ = '1.0'
__maintainer__ = 'Pierre-Yves Langlois'
__status__ = 'Production'
import os
from uadm.uadmcore import *
if __name__ == '__main__':
    mod_conf({'UADM_USE_CENTRIFY': False, 
       'UADM_PAM_SCRIPT_CENTRIFY_ADMINGROUP': 'Domain Admins', 
       'UADM_AUTO_MOUNT_DIR': '/usr/local/bin/auto_mount_www'}, override=False)
    mod_conf({'UADM_DISABLE_MAIL': True})
    admin_group = CONF_MAP['UADM_PAM_SCRIPT_CENTRIFY_ADMINGROUP']
    pam_user = os.getenv('PAM_USER')
    cmd_list = [
     'bash -c \'id %s | grep "27(sudo)\\|0(root)"  2> /dev/null\'' % pam_user]
    if CONF_MAP['UADM_USE_CENTRIFY']:
        cmd_list.append('bash -c \'adquery user %s -A 2> /dev/null | grep "%s"\'' % (pam_user, admin_group))
    is_admin = False
    for c in cmd_list:
        ret = run_cmd(c)
        is_admin = is_admin if ret['return_code'] != 0 else True

    if not is_admin:
        l().info('..chrooting..')
        cmd_list = [
         'mkdir -p /home/%(user)s' % {'user': pam_user},
         'chown root:%(user)s /home/%(user)s' % {'user': pam_user},
         'chmod g+rx /home/%(user)s' % {'user': pam_user},
         'run-parts --report --arg="mount" %s' % CONF_MAP['UADM_AUTO_MOUNT_DIR']]
        exec_cmd_list(cmd_list)