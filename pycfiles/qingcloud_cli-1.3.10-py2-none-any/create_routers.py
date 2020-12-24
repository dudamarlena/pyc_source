# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/router/create_routers.py
# Compiled at: 2017-07-19 00:56:15
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateRoutersAction(BaseAction):
    action = 'CreateRouters'
    command = 'create-routers'
    usage = '%(prog)s [-c <count>] [-N <router_name>] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-c', '--count', dest='count', action='store', type=int, default=1, help='the number of routers to create.')
        parser.add_argument('-N', '--router_name', dest='router_name', action='store', type=str, default='', help='the short name of routers')
        parser.add_argument('-s', '--security_group', dest='security_group', action='store', type=str, default='', help='ID of the security group you want to apply to router, use default security group if not specified')
        parser.add_argument('-n', '--vpc_network', dest='vpc_network', action='store', type=str, default=None, help='VPC IP addresses range, currently support "192.168.0.0/16" or "172.16.0.0/16", required in zone pek3a')
        parser.add_argument('-t', '--router_type', dest='router_type', action='store', type=int, default=1, help='0 - Medium, 1 - Small, 2 - large, 3 - extra-large')
        return

    @classmethod
    def build_directive(cls, options):
        required_params = {'router_name': options.router_name}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        return {'count': options.count, 
           'router_name': options.router_name, 
           'security_group': options.security_group, 
           'vpc_network': options.vpc_network, 
           'router_type': options.router_type}