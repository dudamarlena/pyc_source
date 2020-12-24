# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/grant_resource_groups_to_user_groups.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.iaas_client.actions.base import BaseAction
import json

class GrantResourceGroupsToUserGroupsAction(BaseAction):
    action = 'GrantResourceGroupsToUserGroups'
    command = 'grant-resource-groups-to-user-groups'
    usage = '%(prog)s [-r <rur_set>] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--rur-set', dest='rur_set', action='store', type=str, default='', help="a list of JSON Object which contains 'ID of resource group',                                  'ID of user group' and 'ID of group role'.                                  'For Example:'                                  '[{'resource_group': 'rg-xxxxx', 'user_group': 'ug-xxxxx', 'group_role': 'gr-xxxxx','priority': '2', 'protocol': 'tcp'}]'.")

    @classmethod
    def build_directive(cls, options):
        if options.rur_set == '':
            print 'error: rur_set should be specified'
            return None
        else:
            directive = {'rur_set': json.loads(options.rur_set)}
            return directive