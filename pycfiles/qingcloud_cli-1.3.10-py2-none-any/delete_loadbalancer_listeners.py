# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/lb/delete_loadbalancer_listeners.py
# Compiled at: 2015-05-26 14:06:44
from qingcloud.cli.iaas_client.actions.base import BaseAction
from qingcloud.cli.misc.utils import explode_array

class DeleteLoadBalancerListenersAction(BaseAction):
    action = 'DeleteLoadBalancerListeners'
    command = 'delete-loadbalancer-listeners'
    usage = '%(prog)s -s <lb_listeners> [-f <conf_file>]'
    description = 'Delete one or more load balancer listeners'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--lb_listeners', dest='lb_listeners', action='store', type=str, default='', help='the comma separated IDs of listeners you want to delete.')

    @classmethod
    def build_directive(cls, options):
        required_params = {'lb_listeners': options.lb_listeners}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        return {'loadbalancer_listeners': explode_array(options.lb_listeners)}