# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/delete_user_group_members.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteUserGroupMembersAction(BaseAction):
    action = 'DeleteUserGroupMembers'
    command = 'delete-user-group-members'
    usage = '%(prog)s [-g <user_group> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-g', '--user-group', dest='user_group', action='store', type=str, default='', help='the ID of the user group.')
        parser.add_argument('-u', '--users', dest='users', action='store', type=str, default='', help='An array including IDs of users which you want to delete.')

    @classmethod
    def build_directive(cls, options):
        if options.user_group == '':
            print 'error: user_group should be specified'
            return None
        else:
            users = explode_array(options.users)
            if not users:
                print 'error: users should be specified'
                return None
            directive = {'user_group': options.user_group, 
               'users': users}
            return directive