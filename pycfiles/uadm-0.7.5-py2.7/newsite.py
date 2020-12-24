# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uadm/newsite.py
# Compiled at: 2012-07-09 09:51:34
__author__ = 'Pierre-Yves Langlois'
__copyright__ = 'https://github.com/pylanglois/uadm/blob/master/LICENCE'
__credits__ = ['Pierre-Yves Langlois']
__license__ = 'BSD'
__version__ = '1.0'
__maintainer__ = 'Pierre-Yves Langlois'
__status__ = 'Production'
import sys, re, imp
from string import Template
from uadm.uadmcore import *

def get_input_string(prompt, default_val=None):
    prompt = (default_val or prompt) + ' ' if 1 else prompt + ' [%s] ' % default_val
    user_in = raw_input(prompt)
    if default_val is not None and user_in == '':
        user_in = default_val
    return user_in


def get_input_choices(prompt, choices_list):
    str_choices = ''
    default_val = None
    for c in choices_list:
        str_choices += c + '/'
        if c.isupper():
            default_val = c

    prompt = prompt + ' [%s] ' % str_choices[:len(str_choices) - 1]
    user_in = None
    retry = 0
    while retry < 3 and user_in is None:
        user_in = raw_input(prompt)
        if default_val is not None and user_in == '':
            user_in = default_val
        if user_in not in choices_list and user_in.upper() not in choices_list:
            user_in = None
        retry += 1

    if user_in is None:
        print 'Error. Valid answer are: %s' % choices_list
        exit(1)
    return user_in.lower()


def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1:] == '.':
        hostname = hostname[:-1]
    allowed = re.compile('(?!-)[A-Z\\d-]{1,63}(?<!-)$', re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split('.'))


def build_vhost(admin_mail, site_name, add_www_redirect):
    server_name_alias = ''
    rewrite_cond = ''
    site_url = ''
    if add_www_redirect == 'y':
        server_name_alias = str('        ServerName www.%(site_name)s\n        ServerAlias %(site_name)s\n        ServerAlias dev.www.%(site_name)s\n' % {'site_name': site_name})
        rewrite_cond = str('        RewriteEngine on\n        RewriteCond %(http_post)s ^%(site_rewrite_cond)s$ [NC]\n        RewriteRule ^(.*)$ http://www.%(site_name)s$1 [R=301,L]\n' % {'http_post': '%{HTTP_HOST}', 
           'site_rewrite_cond': site_name.replace('.', '\\.'), 
           'site_name': site_name})
        site_url = 'www.%s' % site_name
    else:
        server_name_alias = str('        ServerName %(site_name)s\n        ServerAlias dev.%(site_name)s\n' % {'site_name': site_name})
        site_url = site_name
    vhost_template = Template(open(get_rel_path('template_vhost')).read())
    vhost = vhost_template.safe_substitute(admin_mail=admin_mail, server_name_alias=server_name_alias, rewrite_cond=rewrite_cond, site_url=site_url)
    logrotate_template = Template(open(get_rel_path('template_logrotate')).read())
    logrotate = logrotate_template.safe_substitute(site_url=site_url)
    index_template = Template(open(get_rel_path('template_index')).read())
    index = index_template.safe_substitute(site_url=site_url)
    return (
     vhost, logrotate, index, site_url)


def create_file(full_path, content):
    try:
        f = open(full_path, 'w+')
        f.write(content)
        f.close()
    except Exception as err:
        l().exception('Creation of file "%s" failed! %s' % (full_path, err))


def run(args=[]):
    mod_conf({'UADM_DISABLE_MAIL': True})
    mod_conf({'UADM_DOCROOT': '/var/www', 
       'UADM_APACHE_VHOST_DIR': '/etc/apache2/sites-available', 
       'UADM_LOGROTATE_DIR': '/etc/logrotate.d', 
       'UADM_USE_CENTRIFY': False}, override=False)
    admin_mail = CONF_MAP['UADM_SRC_EMAIL']
    site_name = args[1] if len(args) > 1 else HOST_INFO['hostname']
    add_www_redirect = ['Y', 'n']
    use_auto_mount = ['Y', 'n']
    www_root_sec_group = None
    www_root_sec_group_create = ['y', 'N']
    admin_mail = get_input_string('What is the server admin email (yours)?', admin_mail)
    site_name = get_input_string('What is the dns name of the new site?', site_name)
    if not is_valid_hostname(site_name):
        print "'%s' is not a valid hostname!!!" % site_name
        exit(1)
    if not site_name.startswith('www.'):
        choices = add_www_redirect
        add_www_redirect = get_input_choices('Do you want to redirect %s to www.%s automatically?' % (site_name, site_name), add_www_redirect)
    else:
        add_www_redirect = 'n'
    www_root_sec_group = get_input_string('Which unix/centrify group will be use to grant the access to document root directory?', site_name)
    www_root_sec_group_create = get_input_choices(str('Do you want to create a unix group for %s? If no, make sure that the group exists or the script will fail.' % www_root_sec_group), www_root_sec_group_create)
    use_auto_mount = get_input_choices('Do you want use auto mount in /home/user/%s?' % site_name, use_auto_mount)
    ready_to_go = '\n    OK, ready to go. Are those info correct?\n\n    admin_mail = %(admin_mail)s\n    site_name = %(site_name)s\n    add_www_redirect = %(add_www_redirect)s\n    use_auto_mount = %(use_auto_mount)s\n    www_root_sec_group = %(www_root_sec_group)s\n    www_root_sec_group_create = %(www_root_sec_group_create)s\n\n>>>' % {'admin_mail': admin_mail, 
       'site_name': site_name, 
       'add_www_redirect': add_www_redirect, 
       'use_auto_mount': use_auto_mount, 
       'www_root_sec_group': www_root_sec_group, 
       'www_root_sec_group_create': www_root_sec_group_create}
    ready = get_input_choices(ready_to_go, ['Y', 'n'])
    if ready == 'y':
        try:
            cmd_list = ['bash -c \'cat /etc/group | grep "%s"  2> /dev/null\'' % www_root_sec_group.replace('.', '\\.')]
            if CONF_MAP['UADM_USE_CENTRIFY']:
                cmd_list.append("bash -c 'adquery group %s > /dev/null 2>&1'" % www_root_sec_group)
            group_exists = False
            for c in cmd_list:
                ret = run_cmd(c)
                group_exists = group_exists if group_exists != 0 else ret['return_code'] != 0

            if not group_exists:
                l().error('The centrify/unix group %s does not exists!!! Creation is aborted...' % www_root_sec_group)
                exit(1)
            vhost, logrotate, index, site_url = build_vhost(admin_mail, site_name, add_www_redirect)
            root_dir = '%s/%s' % (CONF_MAP['UADM_DOCROOT'], site_url)
            cmd_list = [
             str('mkdir -p %s/logs' % root_dir),
             str('chown -R www-data:www-data %s' % root_dir),
             str('setfacl -R    -m g:%s:rwx %s' % (www_root_sec_group, root_dir)),
             str('setfacl -R -d -m g:%s:rwx %s' % (www_root_sec_group, root_dir))]
            completed, ret_map = exec_cmd_list(cmd_list)
            if not completed:
                exit(1)
            fname = '%s/index.html' % root_dir
            create_file(fname, index)
            fname = '%s/%s' % (CONF_MAP['UADM_APACHE_VHOST_DIR'], site_url)
            create_file(fname, vhost)
            fname = '%s/%s' % (CONF_MAP['UADM_LOGROTATE_DIR'], site_url)
            create_file(fname, logrotate)
            cmd_list = [
             str('a2ensite  %s' % site_url),
             str('apache2ctl graceful')]
            completed, ret_map = exec_cmd_list(cmd_list)
            if not completed:
                exit(1)
            if use_auto_mount == 'y':
                cmd_list = [
                 str('mkdir -p %s' % CONF_MAP['UADM_AUTO_MOUNT_DIR'])]
                completed, ret_map = exec_cmd_list(cmd_list)
                if not completed:
                    exit(1)
                auto_mount_template = Template(open(get_rel_path('auto_mount_template.py')).read())
                auto_mount = auto_mount_template.safe_substitute(template_site_name=site_name, template_group_name=www_root_sec_group)
                fname = '%s/%s' % (CONF_MAP['UADM_AUTO_MOUNT_DIR'], site_url.replace('.', '_'))
                create_file(fname, auto_mount)
                cmd_list = [
                 str('chmod +x %s' % fname)]
                completed, ret_map = exec_cmd_list(cmd_list)
                if not completed:
                    exit(1)
        except Exception as err:
            l().exception('Exception of fire! %s' % err)

    return


if __name__ == '__main__':
    run(sys.argv)