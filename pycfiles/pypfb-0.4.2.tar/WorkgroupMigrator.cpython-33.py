# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/printflow2/WorkgroupMigrator.py
# Compiled at: 2014-04-03 03:33:52
# Size of source mod 2**32: 3125 bytes
__doc__ = '\nCreated on Jan 31, 2014\n\n@author: "Colin Manning"\n'
from .JDs import JDs
import os, getopt, sys
from django.core.exceptions import ObjectDoesNotExist
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from workgroups.models import Workgroup, Client, User

def main():
    workgroupId = None
    help_text = 'usage:\n workgroup_migrator -w <workgroup>'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vhc:w', ['workgroup='])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-w', '--workgroup'):
            workgroupId = arg
            continue

    jds = JDs('/opt/printflow2/db', 503, 502)
    jds.register_class('workgroup')
    try:
        json_workgroup = jds.fetch('workgroup', workgroupId)
        try:
            dj_workgroup = Workgroup.objects.get(noosh_id=workgroupId)
        except ObjectDoesNotExist:
            dj_workgroup = Workgroup()
            dj_workgroup.noosh_id = json_workgroup['id']
            dj_workgroup.name = json_workgroup['name']
            dj_workgroup.os_user_name = json_workgroup['os_user_name']
            dj_workgroup.os_group_name = json_workgroup['os_group_name']
            dj_workgroup.os_userid = json_workgroup['os_userid']
            dj_workgroup.os_groupid = json_workgroup['os_groupid']
            dj_workgroup.preflight_profile = json_workgroup['preflight_profile']
            dj_workgroup.dropbox_root = json_workgroup['dropbox_root']
            dj_workgroup.serial_number = json_workgroup['serial_number']
            dj_workgroup.dam_site = json_workgroup['dam_site']
            dj_workgroup.last_check = json_workgroup['last_check']
            if json_workgroup['id_parent'] > 0:
                try:
                    p = Workgroup.objects.get(noosh_id=json_workgroup['id_parent'])
                    dj_workgroup.parent = p
                except ObjectDoesNotExist:
                    pass

            dj_workgroup.save()
            for json_client in json_workgroup['clients']:
                dj_client = Client()
                dj_client.name = json_client['name']
                dj_client.save()
                for json_user in json_client['users']:
                    try:
                        dj_user = User.objects.get(email=json_client['email'])
                    except ObjectDoesNotExist:
                        dj_user.first_name = json_user['first_name']
                        dj_user.last_name = json_user['last_name']
                        dj_user.email = json_user['email']
                        dj_user.noosh_username = json_user['noosh_username']
                        dj_user.dropbox_name = json_user['dropbox_name']
                        dj_user = User()

                    dj_user.save()
                    dj_client.users.add(dj_user)
                    dj_client.save()

                dj_workgroup.clients.add(dj_client)

    except:
        print('problem getting workgroup with id: ', workgroupId)

    return


if __name__ == '__main__':
    main()