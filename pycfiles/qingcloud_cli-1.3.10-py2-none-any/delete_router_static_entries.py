# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/router/delete_router_static_entries.py
# Compiled at: 2016-07-18 23:48:49
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteRouterStaticEntriesAction(BaseAction):
    action = 'DeleteRouterStaticEntries'
    command = 'delete-router-static-entries'
    usage = '%(prog)s -e "router_static_entry_id, ..." [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-e', '--router_static_entries', dest='router_static_entries', action='store', type=str, default='', help='the comma separated IDs of router static entries you want to delete. ')

    @classmethod
    def build_directive(cls, options):
        router_static_entries = explode_array(options.router_static_entries)
        if not router_static_entries:
            return None
        else:
            return {'router_static_entries': router_static_entries}