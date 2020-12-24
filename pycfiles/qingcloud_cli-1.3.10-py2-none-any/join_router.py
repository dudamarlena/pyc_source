# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/router/join_router.py
# Compiled at: 2015-05-26 14:08:17
from qingcloud.cli.iaas_client.actions.base import BaseAction

class JoinRouterAction(BaseAction):
    action = 'JoinRouter'
    command = 'join-router'
    usage = '%(prog)s -r <router_id> -v <vxnet_id> -n <ip_network> [-f <features> -m <manager_ip> -S <dyn_ip_start> -E <dyn_ip_end>] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--router', dest='router', action='store', type=str, default='', help='ID of the router which vxnet will join.')
        parser.add_argument('-v', '--vxnet', dest='vxnet', action='store', type=str, default='', help='the id of the vxnet that will join the router.')
        parser.add_argument('-n', '--ip_network', dest='ip_network', action='store', type=str, default='', help='ip for vxnet, e.g. `192.168.x.0/24` ')
        parser.add_argument('-F', '--features', dest='features', action='store', type=int, default=1, help='\n                the integer value of the bit mask that represent the selected features.\n                Masking Bit:\n                1 - dhcp server\n                ')
        parser.add_argument('-m', '--manager_ip', dest='manager_ip', action='store', type=str, default=None, help='the manager ip, this can be used as default gateway within the private network, e.g. "192.168.x.2".')
        parser.add_argument('-S', '--dyn_ip_start', dest='dyn_ip_start', action='store', type=str, default=None, help='starting ip allocated from DHCP server, e.g. "192.168.x.2".')
        parser.add_argument('-E', '--dyn_ip_end', dest='dyn_ip_end', action='store', type=str, default=None, help='ending ip allocated from DHCP server, e.g. "192.168.x.254".')
        return

    @classmethod
    def build_directive(cls, options):
        required_params = {'router': options.router, 
           'vxnet': options.vxnet, 
           'ip_netword': options.ip_network}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        return {'router': options.router, 
           'vxnet': options.vxnet, 
           'features': options.features, 
           'ip_network': options.ip_network, 
           'manager_ip': options.manager_ip, 
           'dyn_ip_start': options.dyn_ip_start, 
           'dyn_ip_end': options.dyn_ip_end}