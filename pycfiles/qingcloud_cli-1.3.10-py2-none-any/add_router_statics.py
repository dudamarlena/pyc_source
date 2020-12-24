# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/router/add_router_statics.py
# Compiled at: 2015-05-26 14:08:07
import json
from qingcloud.cli.iaas_client.actions.base import BaseAction

class AddRouterStaticsAction(BaseAction):
    action = 'AddRouterStatics'
    command = 'add-router-statics'
    usage = '%(prog)s -r <router_id> -s <statics> [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--router', dest='router', action='store', type=str, default='', help='the ID of router you want to add statics to.')
        parser.add_argument('-s', '--statics', dest='statics', action='store', type=str, default='', help='\n                JSON string of static list. e.g.\n                \'[{"static_type":"3","val1":"i-b7zjztrf","val2":"domain-name-servers=8.8.8.8"},{"val4":"tcp","val1":"12","val2":"192.168.1.2","val3":"12","static_type":"1"}]\'\n                ')

    @classmethod
    def build_directive(cls, options):
        required_params = {'router': options.router, 
           'statics': options.statics}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'param [%s] should be specified' % param
                return

        return {'router': options.router, 
           'statics': json.loads(options.statics)}