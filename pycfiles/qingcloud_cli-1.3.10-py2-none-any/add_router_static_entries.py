# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/router/add_router_static_entries.py
# Compiled at: 2016-07-18 12:28:12
import json
from qingcloud.cli.iaas_client.actions.base import BaseAction

class AddRouterStaticEntriesAction(BaseAction):
    action = 'AddRouterStaticEntries'
    command = 'add-router-static-entries'
    usage = '%(prog)s -r <router_static_id> -e <entries> [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--static', dest='static', action='store', type=str, default='', help='the ID of router static you want to add entries to.')
        parser.add_argument('-e', '--entries', dest='entries', action='store', type=str, default='', help='\n                JSON string of static entry list. e.g.\n                \'[{"val1":"vpn username","val2":"vpn passwd"}]\'\n                ')

    @classmethod
    def build_directive(cls, options):
        required_params = {'static': options.static, 
           'entries': options.entries}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'param [%s] should be specified' % param
                return

        return {'router_static': options.static, 
           'entries': json.loads(options.entries)}