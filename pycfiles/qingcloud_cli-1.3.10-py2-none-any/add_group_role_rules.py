# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/add_group_role_rules.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class AddGroupRoleRulesAction(BaseAction):
    action = 'AddGroupRoleRules'
    command = 'add-group-role-rules'
    usage = '%(prog)s [-r <group_role> ...] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--group-role', dest='group_role', action='store', type=str, default='', help='the ID of the group role.')
        parser.add_argument('-p', '--policy', dest='policy', action='store', type=str, default='', help="the policy whose format is 'resource_typeor.operation_type',                                  See: https://docs.qingcloud.com/api/resource_acl/AddGroupRoleRules.html.")
        parser.add_argument('-d', '--description', dest='description', action='store', type=str, default=None, help='the description of rule.')
        return

    @classmethod
    def build_directive(cls, options):
        if options.group_role == '':
            print 'error: group_role should be specified'
            return None
        else:
            if options.policy == '':
                print 'error: policy should be specified'
                return None
            directive = {'group_role': options.group_role, 
               'policy': options.policy, 
               'description': options.description}
            return directive