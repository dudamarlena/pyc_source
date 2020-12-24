# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/describe_shared_resource_groups.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeSharedResourceGroupsAction(BaseAction):
    action = 'DescribeSharedResourceGroups'
    command = 'describe-shared-resource-groups'
    usage = '%(prog)s [-r <resource_groups> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--resource-groups', dest='resource_groups', action='store', type=str, default=None, help='An array including IDs of resource groups.')
        parser.add_argument('-o', '--owner', dest='owner', action='store', type=str, default=None, help='The people who shares resource groups with oneself.')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'resource_groups': explode_array(options.resource_groups), 
           'owner': options.owner}
        return directive