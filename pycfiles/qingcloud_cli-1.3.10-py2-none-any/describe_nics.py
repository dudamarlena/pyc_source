# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/nic/describe_nics.py
# Compiled at: 2017-05-07 03:49:33
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeNicsAction(BaseAction):
    action = 'DescribeNics'
    command = 'describe-nics'
    usage = '%(prog)s -n "nic_id,..." [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-n', '--nics', dest='nics', action='store', type=str, default='', help='the comma separated IDs of nics you want to describe.')
        parser.add_argument('-x', '--vxnets', dest='vxnets', action='store', type=str, default='', help='the comma separated IDs of vxnet which nic attached.')
        parser.add_argument('-t', '--vxnet-type', dest='vxnet_type', action='store', type=str, default=None, help='the type of vxnet, 0: unmanaged, 1: managed.')
        parser.add_argument('-s', '--status', dest='status', action='store', type=str, default='', help='nic status: available, in-use.')
        parser.add_argument('-N', '--nic-name', dest='nic_name', action='store', type=str, default='', help='the name of nic')
        return

    @classmethod
    def build_directive(cls, options):
        return {'nics': explode_array(options.nics), 
           'status': explode_array(options.status), 
           'nic_name': options.nic_name, 
           'vxnets': explode_array(options.vxnets), 
           'vxnet_type': explode_array(options.vxnet_type), 
           'offset': options.offset, 
           'limit': options.limit}