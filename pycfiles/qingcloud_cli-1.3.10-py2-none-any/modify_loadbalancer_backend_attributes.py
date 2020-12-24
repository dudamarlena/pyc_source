# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/lb/modify_loadbalancer_backend_attributes.py
# Compiled at: 2015-09-14 23:09:31
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyLoadBalancerBackendAttributesAction(BaseAction):
    action = 'ModifyLoadBalancerBackendAttributes'
    command = 'modify-loadbalancer-backend-attributes'
    usage = '%(prog)s -b <lb_backend> [-p <port> -w <weight> -f <conf_file>]'
    description = 'Modify load balancer backend attributes.'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-b', '--lb_backend', dest='lb_backend', action='store', type=str, default='', help='the ID of load balancer backend.')
        parser.add_argument('-p', '--port', dest='port', action='store', type=int, default=None, help='the backend port.')
        parser.add_argument('-w', '--weight', dest='weight', action='store', type=int, default=None, help='the backend weight, valid value is from 1 to 100.')
        parser.add_argument('--disabled', dest='disabled', action='store', type=int, default=None, help='disable this backend or not, 0: enable, 1: disable.')
        parser.add_argument('-N', '--name', dest='name', action='store', type=str, default=None, help='new backend name')
        return

    @classmethod
    def build_directive(cls, options):
        if not options.lb_backend:
            print 'error: backend should be specified'
            return None
        else:
            return {'loadbalancer_backend': options.lb_backend, 
               'loadbalancer_backend_name': options.name, 
               'port': options.port, 
               'weight': options.weight, 
               'disabled': options.disabled}