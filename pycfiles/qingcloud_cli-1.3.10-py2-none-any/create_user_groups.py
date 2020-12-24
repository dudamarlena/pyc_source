# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/create_user_groups.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateUserGroupsAction(BaseAction):
    action = 'CreateUserGroups'
    command = 'create-user-groups'
    usage = '%(prog)s [-n <user_group_name> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-n', '--user-group-name', dest='user_group_name', action='store', type=str, default=None, help='the name of user groups.')
        parser.add_argument('-d', '--description', dest='description', action='store', type=str, default=None, help='the description of user groups.')
        parser.add_argument('-c', '--count', dest='count', action='store', type=int, default=1, help='the number of user groups created at one time,defaults 1.')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'user_group_name': options.user_group_name, 
           'description': options.description, 
           'count': options.count}
        return directive