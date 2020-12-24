# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/router/modify_router_static_entry_attributes.py
# Compiled at: 2016-07-18 22:21:37
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyRouterStaticEntryAttributesAction(BaseAction):
    action = 'ModifyRouterStaticEntryAttributes'
    command = 'modify-router-static-entry-attributes'
    usage = '%(prog)s -s <router_static_entry_id> [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-e', '--router-static-entry', dest='router_static_entry', action='store', type=str, default=None, help='the ID of router static entry you want to modify.')
        parser.add_argument('-N', '--name', dest='router_static_entry_name', action='store', type=str, default=None, help='the name of router static entry.')
        parser.add_argument('--val1', dest='val1', action='store', type=str, default=None, help='the val1')
        parser.add_argument('--val2', dest='val2', action='store', type=str, default=None, help='the val2')
        return

    @classmethod
    def build_directive(cls, options):
        if not options.router_static_entry:
            print 'error: [router-static-entry] should be specified.'
            return None
        else:
            directive = {'router_static_entry': options.router_static_entry, 
               'router_static_entry_name': options.router_static_entry_name, 
               'val1': options.val1, 
               'val2': options.val2}
            return directive