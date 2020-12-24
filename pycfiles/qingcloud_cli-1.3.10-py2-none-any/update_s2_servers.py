# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/update_s2_servers.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class UpdateS2ServersAction(BaseAction):
    action = 'UpdateS2Servers'
    command = 'update-s2-servers'
    usage = '%(prog)s -s <s2_servers>  [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--s2-servers', dest='s2_servers', action='store', type=str, default=None, help='the IDs of s2 servers you want to update.')
        return

    @classmethod
    def build_directive(cls, options):
        for key in ['s2_servers']:
            if not hasattr(options, key):
                print 'error: [%s] should be specified.' % key
                return None

        directive = {'s2_servers': explode_array(options.s2_servers)}
        return directive