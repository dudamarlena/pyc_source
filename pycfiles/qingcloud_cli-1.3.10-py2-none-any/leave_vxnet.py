# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/vxnet/leave_vxnet.py
# Compiled at: 2015-05-26 14:09:47
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class LeaveVxnetAction(BaseAction):
    action = 'LeaveVxnet'
    command = 'leave-vxnet'
    usage = '%(prog)s --instances "instance_id, ..." --vxnet <vxnet_id> [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-i', '--instances', dest='instances', action='store', type=str, default='', help='the IDs of instances that will leave a vxnet.')
        parser.add_argument('-v', '--vxnet', dest='vxnet', action='store', type=str, default='', help='the ID of the vxnet the instances will leave. ')

    @classmethod
    def build_directive(cls, options):
        instances = explode_array(options.instances)
        if not options.vxnet or not instances:
            print 'error: [instances] and [vxnet] should be specified'
            return None
        else:
            return {'vxnet': options.vxnet, 
               'instances': instances}