# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/lb/create_loadbalancer.py
# Compiled at: 2017-09-21 02:37:46
from qingcloud.cli.iaas_client.actions.base import BaseAction
from qingcloud.cli.misc.utils import explode_array

class CreateLoadBalancerAction(BaseAction):
    action = 'CreateLoadBalancer'
    command = 'create-loadbalancer'
    usage = '%(prog)s -e <eips> [-n <name> -s <sg> -f <conf_file>]'
    description = 'Associate one or more eips with load balancer'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-t', '--loadbalancer_type', dest='loadbalancer_type', action='store', type=int, default='0', help='the type of load balancer.')
        parser.add_argument('-e', '--eips', dest='eips', action='store', type=str, default='', help='the comma separated IDs of eips you want to associate.')
        parser.add_argument('-x', '--vxnet', dest='vxnet', action='store', type=str, default='', help='The vxnet id you want create lb to.')
        parser.add_argument('-p', '--private_ip', dest='private_ip', action='store', type=str, help='Specify the private ip.', default='')
        parser.add_argument('-N', '--name', dest='name', action='store', type=str, default='', help='load balancer name.')
        parser.add_argument('-s', '--sg', dest='sg', action='store', type=str, default=None, help='the ID of security group which will be applied to load balancer.')
        parser.add_argument('-c', '--node_count', dest='node_count', action='store', type=int, default=None, help='the number of nodes in load balancer cluster.')
        parser.add_argument('--target-user', dest='target_user', action='store', type=str, default=None, help='ID of user who will own this resource, should be one of your sub-account.')
        return

    @classmethod
    def build_directive(cls, options):
        required_params = {'eips': options.eips, 
           'vxnet': options.vxnet}
        if not required_params['eips'] and not required_params['vxnet']:
            print 'error: [eips] or [vxnet] should be specified one'
            return None
        else:
            return {'eips': explode_array(options.eips), 
               'vxnet': options.vxnet, 
               'private_ip': options.private_ip, 
               'loadbalancer_name': options.name, 
               'loadbalancer_type': options.loadbalancer_type, 
               'security_group': options.sg, 
               'node_count': options.node_count, 
               'target_user': options.target_user}