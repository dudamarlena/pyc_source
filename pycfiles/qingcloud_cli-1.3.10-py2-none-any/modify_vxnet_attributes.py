# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/vxnet/modify_vxnet_attributes.py
# Compiled at: 2015-05-26 14:09:48
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyVxnetAttributesAction(BaseAction):
    action = 'ModifyVxnetAttributes'
    command = 'modify-vxnet-attributes'
    usage = '%(prog)s [-v <vxnet_id>] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-v', '--vxnet_id', dest='vxnet_id', action='store', type=str, default='', help='the ID of the vxnet whose attributes you want to modify.')
        parser.add_argument('-N', '--vxnet_name', dest='vxnet_name', action='store', type=str, default=None, help='specify the new vxnet name.')
        parser.add_argument('-D', '--description', dest='description', action='store', type=str, default=None, help='the detailed description of the resource')
        return

    @classmethod
    def build_directive(cls, options):
        if not options.vxnet_id:
            return None
        else:
            return {'vxnet': options.vxnet_id, 
               'vxnet_name': options.vxnet_name, 
               'description': options.description}