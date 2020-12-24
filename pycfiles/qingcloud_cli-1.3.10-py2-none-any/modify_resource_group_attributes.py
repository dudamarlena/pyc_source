# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/collaboration/modify_resource_group_attributes.py
# Compiled at: 2018-01-10 23:45:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyResourceGroupAttributesAction(BaseAction):
    action = 'ModifyResourceGroupAttributes'
    command = 'modify-resource-group-attributes'
    usage = '%(prog)s [-r <resource_group>] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--resource-group', dest='resource_group', action='store', type=str, default='', help='The ID of resource group which attributes you want to modify.')
        parser.add_argument('-n', '--resource-group-name', dest='resource_group_name', action='store', type=str, default=None, help='The new name of the resource group which will be modified.')
        parser.add_argument('-d', '--description', dest='description', action='store', type=str, default=None, help='The description of the resource group.')
        return

    @classmethod
    def build_directive(cls, options):
        if options.resource_group == '':
            print 'error: resource_group should be specified'
            return None
        else:
            directive = {'resource_group': options.resource_group, 
               'description': options.description, 
               'resource_group_name': options.resource_group_name}
            return directive