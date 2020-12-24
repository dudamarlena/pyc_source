# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/delete_resource_group_items.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteResourceGroupItemsAction(BaseAction):
    action = 'DeleteResourceGroupItems'
    command = 'delete-resource-group-items'
    usage = '%(prog)s [-g <resource_group> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-g', '--resource-group', dest='resource_group', action='store', type=str, default='', help='the ID of the resource group.')
        parser.add_argument('-r', '--resources', dest='resources', action='store', type=str, default='', help='An array including IDs of resources which you want to delete.')

    @classmethod
    def build_directive(cls, options):
        if options.resource_group == '':
            print 'error: resource_group should be specified'
            return None
        else:
            resources = explode_array(options.resources)
            if not resources:
                print 'error: resources should be specified'
                return None
            directive = {'resource_group': options.resource_group, 
               'resources': resources}
            return directive