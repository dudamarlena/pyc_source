# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/create_group_roles.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateGroupRolesAction(BaseAction):
    action = 'CreateGroupRoles'
    command = 'create-group-roles'
    usage = '%(prog)s [-t <role_type>] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-t', '--role-type', dest='role_type', action='store', type=str, default='', help="the type of role, Currently only support 'rule'.")
        parser.add_argument('-n', '--group-role-name', dest='group_role_name', action='store', type=str, default=None, help='the name of group role.')
        parser.add_argument('-d', '--description', dest='description', action='store', type=str, default=None, help='the description of group role.')
        parser.add_argument('-c', '--count', dest='count', action='store', type=int, default=1, help='the number of user roles created at one time,defaults 1.')
        return

    @classmethod
    def build_directive(cls, options):
        if options.role_type == '':
            print 'error: role_type should be specified'
            return None
        else:
            directive = {'role_type': options.role_type, 
               'group_role_name': options.group_role_name, 
               'description': options.description, 
               'count': options.count}
            return directive