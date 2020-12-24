# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/change_s2_server_vxnet.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ChangeS2ServerVxnetAction(BaseAction):
    action = 'ChangeS2ServerVxnet'
    command = 'change-s2-server-vxnet'
    usage = '%(prog)s -s <s2_server> -v <vxnet> [-p <private_ip> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--s2-server', dest='s2_server', action='store', type=str, default=None, help='the ID of s2 server.')
        parser.add_argument('-v', '--vxnet', dest='vxnet', action='store', type=str, default=None, help='the ID of vxnet.')
        parser.add_argument('-p', '--private-ip', dest='private_ip', action='store', type=str, default=None, help='you may specify the ip address of this server.')
        return

    @classmethod
    def build_directive(cls, options):
        for key in ['s2_server', 'vxnet']:
            if not hasattr(options, key):
                print 'error: [%s] should be specified.' % key
                return None

        directive = {'s2_server': options.s2_server, 'vxnet': options.vxnet, 
           'private_ip': options.private_ip}
        return directive