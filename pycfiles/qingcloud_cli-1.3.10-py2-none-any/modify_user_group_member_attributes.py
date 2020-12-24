# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/modify_user_group_member_attributes.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyUserGroupMemberAttributesAction(BaseAction):
    action = 'ModifyUserGroupMemberAttributes'
    command = 'modify-user-group-member-attributes'
    usage = '%(prog)s [-g <user_group>...] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-g', '--user-group', dest='user_group', action='store', type=str, default='', help='The ID of user group which attributes you want to modify.')
        parser.add_argument('-u', '--user', dest='user', action='store', type=str, default='', help='The ID of user which will be modified.')
        parser.add_argument('-r', '--remarks', dest='remarks', action='store', type=str, default=None, help='The description of the user group.')
        parser.add_argument('-s', '--status', dest='status', action='store', type=str, default=None, help='the status of user group.')
        return

    @classmethod
    def build_directive(cls, options):
        if options.user_group == '':
            print 'error: user_group should be specified'
            return None
        else:
            if options.user == '':
                print 'error: user should be specified'
                return None
            directive = {'user_group': options.user_group, 
               'user': options.user, 
               'remarks': options.remarks, 
               'status': options.status}
            return directive