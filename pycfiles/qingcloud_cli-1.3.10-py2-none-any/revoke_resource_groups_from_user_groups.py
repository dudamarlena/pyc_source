# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/revoke_resource_groups_from_user_groups.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction
import json

class RevokeResourceGroupsFromUserGroupsAction(BaseAction):
    action = 'RevokeResourceGroupsFromUserGroups'
    command = 'revoke-resource-groups-from-user-groups'
    usage = '%(prog)s [-r <ru_set>] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--ru-set', dest='ru_set', action='store', type=str, default='', help="a list of JSON Object which contains ID of resource group and ID of user group.                                  'For Example:'                                  '[{'resource_group': 'rg-xxxxx', 'user_group': 'ug-xxxxx', 'priority': '2', 'protocol': 'tcp'}]'.")
        parser.add_argument('-R', '--resource-groups', dest='resource_groups', action='store', type=str, default=None, help='an array including IDs of resource groups.                                   if it is not empty, will revoke all authorization relationships of specified resource groups.')
        parser.add_argument('-u', '--user-groups', dest='user_groups', action='store', type=str, default=None, help='an array including IDs of resource groups.                                   if it is not empty, will revoke all authorization relationships of specified user groups.')
        parser.add_argument('-g', '--group-roles', dest='group_roles', action='store', type=str, default=None, help='an array including IDs of resource groups.                                   if it is not empty, will revoke all authorization relationships of specified group roles.')
        return

    @classmethod
    def build_directive(cls, options):
        if options.ru_set == '':
            print 'error: ru_set should be specified'
            return None
        else:
            directive = {'ru_set': json.loads(options.ru_set), 
               'resource_groups': explode_array(options.resource_groups), 
               'user_groups': explode_array(options.user_groups), 
               'group_roles': explode_array(options.group_roles)}
            return directive