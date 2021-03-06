# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/lb/add_loadbalancer_listeners.py
# Compiled at: 2015-05-26 14:06:37
import json
from qingcloud.cli.iaas_client.actions.base import BaseAction

class AddLoadBalancerListenersAction(BaseAction):
    action = 'AddLoadBalancerListeners'
    command = 'add-loadbalancer-listeners'
    usage = '%(prog)s -l <loadbalancer> -s <listeners> [-f <conf_file>]'
    description = 'Add one or more listeners to load balancer'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-l', '--loadbalancer', dest='loadbalancer', action='store', type=str, default='', help='ID of load balancer which you add listeners to.')
        parser.add_argument('-s', '--listeners', dest='listeners', action='store', type=str, default='', help='JSON string of listener list. e.g. \'                 [{"listener_protocol":"http","listener_port":"80","backend_protocol":"http",                 "balance_mode": "roundrobin", "forwardfor": 0, "healthy_check_method": "tcp",                 "healthy_check_option": "10|5|2|5", "session_sticky": "insert|3600"}]                 \'')

    @classmethod
    def build_directive(cls, options):
        required_params = {'loadbalancer': options.loadbalancer, 
           'listeners': options.listeners}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        return {'loadbalancer': options.loadbalancer, 
           'listeners': json.loads(options.listeners)}