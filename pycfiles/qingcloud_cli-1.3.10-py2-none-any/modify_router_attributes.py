# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/router/modify_router_attributes.py
# Compiled at: 2015-05-26 14:08:20
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyRouterAttributesAction(BaseAction):
    action = 'ModifyRouterAttributes'
    command = 'modify-router-attributes'
    usage = '%(prog)s -r <router_id> [-s <security_group> -e <eip> -v <vxnet> -F <features> -S <dyn_start_ip> -E <dyn_end_ip>] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--router', dest='router', action='store', type=str, default='', help='the id of the router whose attributes you want to modify.')
        parser.add_argument('-e', '--eip', dest='eip', action='store', type=str, default='', help='ID of eip that will apply to the router.')
        parser.add_argument('-s', '--security_group', dest='security_group', action='store', type=str, default='', help='the id of the security_group you want to apply to router.')
        parser.add_argument('-N', '--router_name', dest='router_name', action='store', type=str, default=None, help='new router_name.')
        parser.add_argument('-D', '--description', dest='description', action='store', type=str, default=None, help='new description.')
        parser.add_argument('-v', '--vxnet', dest='vxnet', action='store', type=str, default=None, help='the id of the vxnet whose feature you want to modify.')
        parser.add_argument('-F', '--features', dest='features', action='store', type=int, default=None, help='\n                the integer value of the bit mask that represent the selected features.\n                Masking Bit:\n                1 - dhcp server\n                ')
        parser.add_argument('-S', '--dyn_ip_start', dest='dyn_ip_start', action='store', type=str, default=None, help='starting ip allocated from DHCP server, e.g. "192.168.x.2".')
        parser.add_argument('-E', '--dyn_ip_end', dest='dyn_ip_end', action='store', type=str, default=None, help='ending ip allocated from DHCP server, e.g. "192.168.x.254".')
        return

    @classmethod
    def build_directive(cls, options):
        if not options.router:
            print 'error: [router] should be specified.'
            return
        else:
            if options.features is not None and not options.vxnet:
                print 'error: [vxnet] should be specified if modify features.'
                return
            if (options.dyn_ip_start or options.dyn_ip_end) and options.features is None:
                print 'error: [features] should be specified if modify ip range.'
                return
            return {'router': options.router, 
               'router_name': options.router_name, 
               'description': options.description, 
               'eip': options.eip, 
               'security_group': options.security_group, 
               'vxnet': options.vxnet, 
               'features': options.features, 
               'dyn_ip_start': options.dyn_ip_start, 
               'dyn_ip_end': options.dyn_ip_end}