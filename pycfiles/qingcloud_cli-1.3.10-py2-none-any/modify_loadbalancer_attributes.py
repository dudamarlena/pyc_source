# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/lb/modify_loadbalancer_attributes.py
# Compiled at: 2015-05-26 14:07:01
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyLoadBalancerAttributesAction(BaseAction):
    action = 'ModifyLoadBalancerAttributes'
    command = 'modify-loadbalancer-attributes'
    usage = '%(prog)s -l <loadbalancer> [-g <security_group> -N <name> -f <conf_file>]'
    description = 'Modify load balancer attributes.'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-l', '--loadbalancer', dest='loadbalancer', action='store', type=str, default='', help='the comma separated IDs of load balancers.')
        parser.add_argument('-g', '--security_group', dest='security_group', action='store', type=str, default=None, help='the id of the security group you want to apply to load balancer.')
        parser.add_argument('-N', '--lb_name', dest='lb_name', action='store', type=str, default=None, help='new load balancer name')
        parser.add_argument('-D', '--description', dest='description', action='store', type=str, default=None, help='new load balancer description')
        return

    @classmethod
    def build_directive(cls, options):
        if not options.loadbalancer:
            print 'error: load balancer should be specified'
            return None
        else:
            return {'loadbalancer': options.loadbalancer, 
               'security_group': options.security_group, 
               'loadbalancer_name': options.lb_name, 
               'description': options.description}