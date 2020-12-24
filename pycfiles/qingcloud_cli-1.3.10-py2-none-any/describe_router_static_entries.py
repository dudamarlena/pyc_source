# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/router/describe_router_static_entries.py
# Compiled at: 2016-07-18 22:16:33
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeRouterStaticEntriesAction(BaseAction):
    action = 'DescribeRouterStaticEntries'
    command = 'describe-router-static-entries'
    usage = '%(prog)s [-s "router_static_entry_id, ..."] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-e', '--router_static_entries', dest='router_static_entries', action='store', type=str, default='', help='the comma separated IDs of router_static_entries you want to list. ')
        parser.add_argument('-s', '--router_static', dest='router_static', action='store', type=str, default='', help='filter by router static. ')

    @classmethod
    def build_directive(cls, options):
        directive = {'router_static_entries': explode_array(options.router_static_entries), 
           'router_static': options.router_static, 
           'offset': options.offset, 
           'limit': options.limit}
        return directive