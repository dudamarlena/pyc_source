# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/delete_resource_groups.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteResourceGroupsAction(BaseAction):
    action = 'DeleteResourceGroups'
    command = 'delete-resource-groups'
    usage = '%(prog)s [-r <resource_groups>] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--resource-groups', dest='resource_groups', action='store', type=str, default='', help=' An array including IDs of the resource groups which you want to delete.')

    @classmethod
    def build_directive(cls, options):
        resource_groups = explode_array(options.resource_groups)
        if not resource_groups:
            print 'error: resource_groups should be specified'
            return None
        else:
            directive = {'resource_groups': resource_groups}
            return directive