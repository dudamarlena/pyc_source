# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uadm/auto_mount_template.py
# Compiled at: 2012-07-09 11:39:53
import os
from uadm.uadmcore import *
if __name__ == '__main__':
    mod_conf({'UADM_USE_CENTRIFY': True}, override=False)
    mod_conf({'UADM_DISABLE_MAIL': True})
    site_name = '${template_site_name}'
    site_group = '${template_group_name}'
    pam_user = os.getenv('PAM_USER')
    cmd_list = [
     'bash -c \'id %s | grep "(%s)"  2> /dev/null\'' % (pam_user, site_group)]
    if CONF_MAP['UADM_USE_CENTRIFY']:
        cmd_list.append('bash -c \'adquery group %s -m 2> /dev/null | grep "%s$"\'' % (site_group, pam_user))
    is_member = False
    for c in cmd_list:
        ret = run_cmd(c)
        is_member = is_member if ret['return_code'] != 0 else True

    if is_member:
        cmd_list = ['mkdir -p /home/%(user)s/%(site)s' % {'user': pam_user, 'site': site_name},
         'chown root:root /home/%(user)s/%(site)s' % {'user': pam_user, 'site': site_name},
         'mount --bind /var/www/%(site)s /home/%(user)s/%(site)s' % {'user': pam_user, 'site': site_name}]
        ret = run_cmd("bash -c 'mount | grep /home/%(user)s/%(site)s  2> /dev/null'" % {'user': pam_user, 'site': site_name})
        is_mounted = ret['return_code'] == 0
        if is_mounted:
            cmd_list.insert(0, 'umount /home/%(user)s/%(site)s' % {'user': pam_user, 'site': site_name})
        exec_cmd_list(cmd_list)
    else:
        l().info('NO MEMBERS')