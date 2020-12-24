# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/vxnet/create_vxnets.py
# Compiled at: 2018-04-12 01:06:40
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateVxnetsAction(BaseAction):
    action = 'CreateVxnets'
    command = 'create-vxnets'
    usage = '%(prog)s --count <count> --vxnet_name <vxnet_name> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-c', '--count', dest='count', action='store', type=int, default=1, help='the number of vxnets to create.')
        parser.add_argument('-N', '--vxnet_name', dest='vxnet_name', action='store', type=str, default='', help='the short name of vxnet you want to create.')
        parser.add_argument('-t', '--vxnet_type', dest='vxnet_type', action='store', type=int, default=1, help='the vxnet type. 0: unmanaged vxnet, 1: managed vxnet. Default 1.')
        parser.add_argument('-m', '--mode', dest='mode', action='store', type=int, default=0, help='The vxnet mode. 0: gre+ovs, 1: vxlan+bridge. Default 0.')

    @classmethod
    def build_directive(cls, options):
        if not options.vxnet_name:
            print '[vxnet_name] should be specified.'
            return None
        else:
            return {'vxnet_name': options.vxnet_name, 
               'vxnet_type': options.vxnet_type, 
               'mode': options.mode, 
               'count': options.count}