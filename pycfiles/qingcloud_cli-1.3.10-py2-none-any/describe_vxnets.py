# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/vxnet/describe_vxnets.py
# Compiled at: 2018-04-12 01:10:06
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeVxnetsAction(BaseAction):
    action = 'DescribeVxnets'
    command = 'describe-vxnets'
    usage = '%(prog)s [-v "vxnet_id, ..."] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-v', '--vxnets', dest='vxnets', action='store', type=str, default='', help='the comma separated IDs of vxnets you want to list.')
        parser.add_argument('-t', '--vxnet_type', dest='vxnet_type', action='store', type=int, default=None, help='filter by vxnet type: 0 - unmanaged vxnet, 1 - managed vxnet')
        parser.add_argument('-m', '--mode', dest='mode', action='store', type=int, default=None, help='The vxnet mode. 0: gre+ovs, 1: vxlan+bridge.')
        parser.add_argument('-V', '--verbose', dest='verbose', action='store', type=int, default=0, help='the number to specify the verbose level, larger the number, the more detailed information will be returned.')
        parser.add_argument('-W', '--search_word', dest='search_word', action='store', type=str, default='', help='the combined search column')
        return

    @classmethod
    def build_directive(cls, options):
        return {'vxnets': explode_array(options.vxnets), 
           'vxnet_type': options.vxnet_type, 
           'search_word': options.search_word, 
           'mode': options.mode, 
           'verbose': options.verbose, 
           'offset': options.offset, 
           'limit': options.limit, 
           'tags': explode_array(options.tags)}