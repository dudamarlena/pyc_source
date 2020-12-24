# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/describe_group_role_rules.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeGroupRoleRulesAction(BaseAction):
    action = 'DescribeGroupRoleRules'
    command = 'describe-group-role-rules'
    usage = '%(prog)s [-r <group_role_rules> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--group-role-rules', dest='group_role_rules', action='store', type=str, default=None, help='an array including IDs of group role rules.')
        parser.add_argument('-g', '--group-roles', dest='group_roles', action='store', type=str, default=None, help='an array including IDs of group roles.')
        parser.add_argument('-s', '--status', dest='status', action='store', type=str, default=None, help="an array including status which could be 'disabled' or 'enabled'.")
        parser.add_argument('-v', '--verbose', dest='verbose', action='store', type=int, default=1, help='Whether to return redundant message.if it is 1, return the details of the instance related other resources.')
        parser.add_argument('-k', '--sort-key', dest='sort_key', action='store', type=str, default=None, help='the sort key, which defaults be create_time.')
        parser.add_argument('-R', '--reverse', dest='reverse', action='store', type=int, default=0, help='0 for Ascending order, 1 for Descending order.')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'group_role_rules': explode_array(options.group_role_rules), 
           'group_roles': explode_array(options.group_roles), 
           'status': explode_array(options.status), 
           'verbose': options.verbose, 
           'sort_key': options.sort_key, 
           'reverse': options.reverse, 
           'limit': options.limit, 
           'offset': options.offset}
        return directive