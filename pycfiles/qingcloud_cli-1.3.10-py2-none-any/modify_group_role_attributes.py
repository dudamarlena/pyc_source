# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/modify_group_role_attributes.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyGroupRoleAttributesAction(BaseAction):
    action = 'ModifyGroupRoleAttributes'
    command = 'modify-group-role-attributes'
    usage = '%(prog)s [-r <group_role>] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--group-role', dest='group_role', action='store', type=str, default='', help='The ID of group role which attributes you want to modify.')
        parser.add_argument('-t', '--role-type', dest='role_type', action='store', type=str, default=None, help="The type of role, Currently only support 'rule'.")
        parser.add_argument('-n', '--group-role-name', dest='group_role_name', action='store', type=str, default=None, help='The name of group role.')
        parser.add_argument('-d', '--description', dest='description', action='store', type=str, default=None, help='The description of group role.')
        parser.add_argument('-s', '--status', dest='status', action='store', type=str, default=None, help="The status of group role which could be 'disabled' or 'enabled'.")
        return

    @classmethod
    def build_directive(cls, options):
        if options.group_role == '':
            print 'error: group_role should be specified'
            return None
        else:
            directive = {'group_role': options.group_role, 
               'role_type': options.role_type, 
               'group_role_name': options.group_role_name, 
               'description': options.description, 
               'status': options.status}
            return directive