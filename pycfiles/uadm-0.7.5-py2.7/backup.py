# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uadm/backup.py
# Compiled at: 2012-07-03 11:55:48
__author__ = 'Pierre-Yves Langlois'
__copyright__ = 'https://github.com/pylanglois/uadm/blob/master/LICENCE'
__credits__ = ['Pierre-Yves Langlois']
__license__ = 'BSD'
__version__ = '1.0'
__maintainer__ = 'Pierre-Yves Langlois'
__status__ = 'Production'
import sys, os
from datetime import datetime
from uadm.uadmcore import *
mod_conf({'SMB_DEST': '//your-smb-server.example.com/backup_server$', 
   'MOUNT_PATH': '/media/backup_server', 
   'CRED_PATH': '/root/.credentials'}, override=False)

class NotADirException(Exception):
    pass


def extract_dir(csv_dirs):
    csv_dirs = csv_dirs.split(',')
    all_dirs = True
    for d in csv_dirs:
        if not os.path.isdir(d):
            all_dirs = False
            break

    if not all_dirs:
        msg = 'Params must be directories... params: %s' % csv_dirs
        raise NotADirException(msg)
    return csv_dirs


def build_duplicity_folder_list(dirs_list):
    duplicity_dirs_list = ''
    for d in dirs_list:
        duplicity_dirs_list += '--include=%s ' % d

    return duplicity_dirs_list


def run(args=[]):
    if len(args) != 2:
        msg = 'Missing or extra parameter. Usage: uadm_xxx.py /etc,/var/www,/dir123'
        l().error(msg)
        send_error_report(msg)
        exit(1)
    else:
        try:
            try:
                pathsToBackup = extract_dir(args[1])
                duplicity_dirs_list = build_duplicity_folder_list(pathsToBackup)
                path_dest = '%s/%s' % (CONF_MAP['MOUNT_PATH'], HOST_INFO['hostname'])
                cmd_list = [
                 cfb(str('\n                        mount   -t cifs \n                                -o credentials=%(cred_path)s,iocharset=utf8,codepage=unicode,unicode \n                                %(smb_dest)s \n                                %(mount_path)s\n                        ' % {'cred_path': CONF_MAP['CRED_PATH'], 
                    'mount_path': CONF_MAP['MOUNT_PATH'], 
                    'smb_dest': CONF_MAP['SMB_DEST']})),
                 cfb(str('\n                        /usr/bin/duplicity \n                            --no-encryption \n                            cleanup \n                            --extra-clean \n                            --force \n                            file://%(path_dest)s/\n                        ' % {'path_dest': path_dest})),
                 cfb(str('\n                        /usr/bin/duplicity \n                            --no-encryption \n                            remove-older-than 1M \n                            -v9 \n                            --force \n                            file://%(path_dest)s/\n                        ' % {'path_dest': path_dest})),
                 cfb(str('\n                        /usr/bin/duplicity \n                            --no-encryption \n                            %(full)s \n\t                        --volsize=250 \n                            %(include)s \n                            --exclude=/** \n                            / \n                            file://%(path_dest)s/ \n                        ' % {'full': 'full' if datetime.now().day == 1 else '', 
                    'include': duplicity_dirs_list, 
                    'path_dest': path_dest}))]
            except NotADirException as e:
                msg = 'Something went wrong: %s' % unicode(e)
                l().exception(msg)
                send_error_report(msg)
                exit(1)
            except:
                msg = 'Something went wrong.'
                l().exception(msg)
                send_error_report(msg)
                exit(1)

        finally:
            exec_cmd_list([
             'umount %s' % CONF_MAP['MOUNT_PATH']])


if __name__ == '__main__':
    run(sys.argv)