# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/router/delete_router_statics.py
# Compiled at: 2016-07-18 22:18:06
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteRouterStaticsAction(BaseAction):
    action = 'DeleteRouterStatics'
    command = 'delete-router-statics'
    usage = '%(prog)s -s "router_static_id, ..." [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--router_statics', dest='router_statics', action='store', type=str, default='', help='the comma separated IDs of router_statics you want to delete. ')

    @classmethod
    def build_directive(cls, options):
        router_statics = explode_array(options.router_statics)
        if not router_statics:
            return None
        else:
            return {'router_statics': router_statics}