# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/router/poweroff_routers.py
# Compiled at: 2015-05-26 14:08:23
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class PowerOffRoutersAction(BaseAction):
    action = 'PowerOffRouters'
    command = 'poweroff-routers'
    usage = '%(prog)s -r "router_id, ..." [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--routers', dest='routers', action='store', type=str, default='', help='the comma separated IDs of routers you want to poweroff.')

    @classmethod
    def build_directive(cls, options):
        routers = explode_array(options.routers)
        if not routers:
            return None
        else:
            return {'routers': routers}