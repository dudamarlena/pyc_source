# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/delete_group_role_rules.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteGroupRoleRulesAction(BaseAction):
    action = 'DeleteGroupRoleRules'
    command = 'delete-group-role-rules'
    usage = '%(prog)s [-r <group_role_rules> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--group-role-rules', dest='group_role_rules', action='store', type=str, default=None, help='an array including the IDs of group role rules.')
        parser.add_argument('-R', '--group-roles', dest='group_roles', action='store', type=str, default=None, help='an array including the IDs of group roles.')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'group_role_rules': explode_array(options.group_role_rules), 
           'group_roles': explode_array(options.group_roles)}
        return directive