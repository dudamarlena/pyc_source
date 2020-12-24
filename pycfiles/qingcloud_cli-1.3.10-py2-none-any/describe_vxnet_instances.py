# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/vxnet/describe_vxnet_instances.py
# Compiled at: 2015-05-26 14:09:43
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeVxnetInstancesAction(BaseAction):
    action = 'DescribeVxnetInstances'
    command = 'describe-vxnet-instances'
    usage = '%(prog)s -v <vxnet_id> [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-v', '--vxnet', dest='vxnet', action='store', type=str, default='', help='ID of vxnet whose instances you want to list.')
        parser.add_argument('-m', '--image', dest='image', action='store', type=str, default='', help='filter by ID of image that instance based')
        parser.add_argument('-i', '--instances', dest='instances', action='store', type=str, default='', help='filter by comma separated IDs of instances')
        parser.add_argument('-t', '--instance_type', dest='instance_type', action='store', type=str, default='', help='filter by instance type')
        parser.add_argument('-s', '--status', dest='status', action='store', type=str, default='', help='filter by instance status: pending, running, stopped, suspended, terminated, ceased')

    @classmethod
    def build_directive(cls, options):
        if not options.vxnet:
            print '[vxnet] should be provided'
            return None
        else:
            return {'vxnet': options.vxnet, 
               'image': explode_array(options.image), 
               'instances': explode_array(options.instances), 
               'instance_type': explode_array(options.instance_type), 
               'status': explode_array(options.status), 
               'offset': options.offset, 
               'limit': options.limit}