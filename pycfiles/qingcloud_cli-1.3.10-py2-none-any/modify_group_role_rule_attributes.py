# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/modify_group_role_rule_attributes.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyGroupRoleRuleAttributesAction(BaseAction):
    action = 'ModifyGroupRoleRuleAttributes'
    command = 'modify-group-role-rule-attributes'
    usage = '%(prog)s [-r <group_role_rule>] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--group-role-rule', dest='group_role_rule', action='store', type=str, default='', help='the ID of group role rule whose attributes you want to modify.')
        parser.add_argument('-d', '--description', dest='description', action='store', type=str, default=None, help='the description of group role rule.')
        parser.add_argument('-p', '--policy', dest='policy', action='store', type=str, default=None, help="the policy whose format is 'resource_type' or 'operation_type'.")
        return

    @classmethod
    def build_directive(cls, options):
        if options.group_role_rule == '':
            print 'error: group_role_rule should be specified'
            return None
        else:
            directive = {'group_role_rule': options.group_role_rule, 
               'description': options.description, 
               'policy': options.policy}
            return directive