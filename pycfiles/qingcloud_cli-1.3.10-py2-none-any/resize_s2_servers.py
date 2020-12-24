# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/resize_s2_servers.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ResizeS2ServersAction(BaseAction):
    action = 'ResizeS2Servers'
    command = 'resize-s2-servers'
    usage = '%(prog)s -s <s2_servers> -T <s2_server_type>  [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--s2-servers', dest='s2_servers', action='store', type=str, default=None, help='the IDs of s2 servers you want to resize.')
        parser.add_argument('-T', '--s2-server-type', dest='s2_server_type', action='store', type=int, default=None, help='valid values includes 0, 1, 2, 3.')
        return

    @classmethod
    def build_directive(cls, options):
        for key in ['s2_servers', 's2_server_type']:
            if not hasattr(options, key):
                print 'error: [%s] should be specified.' % key
                return None

        directive = {'s2_servers': explode_array(options.s2_servers), 's2_server_type': options.s2_server_type}
        return directive