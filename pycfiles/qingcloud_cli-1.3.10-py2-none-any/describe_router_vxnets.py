# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/router/describe_router_vxnets.py
# Compiled at: 2015-05-26 14:08:14
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeRouterVxnetsAction(BaseAction):
    action = 'DescribeRouterVxnets'
    command = 'describe-router-vxnets'
    usage = '%(prog)s -r <router_id> [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--router', dest='router', action='store', type=str, default='', help='ID of router whose vxnets you want to list.')
        parser.add_argument('-v', '--vxnet', dest='vxnet', action='store', type=str, default='', help='filter by vxnet ID. ')

    @classmethod
    def build_directive(cls, options):
        if not options.router:
            print 'error: [router] should be specified'
            return None
        else:
            return {'router': options.router, 
               'vxnet': options.vxnet, 
               'offset': options.offset, 
               'limit': options.limit}