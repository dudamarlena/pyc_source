# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/create_s2_server.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateS2ServerAction(BaseAction):
    action = 'CreateS2Server'
    command = 'create-s2-server'
    usage = '%(prog)s -v <vxnet> -T <service_type> [-n <s2_server_name> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-v', '--vxnet', dest='vxnet', action='store', type=str, default=None, help='the ID of vxnet.')
        parser.add_argument('-T', '--service-type', dest='service_type', action='store', type=str, default=None, help='valid values is vsan or vnas.')
        parser.add_argument('-n', '--s2-server-name', dest='s2_server_name', action='store', type=str, default=None, help='the name of s2 server.')
        parser.add_argument('-s', '--s2-server-type', dest='s2_server_type', action='store', type=int, default=None, help='valid values includes 0, 1, 2, 3.')
        parser.add_argument('-p', '--private-ip', dest='private_ip', action='store', type=str, default=None, help='you may specify the ip address of this server.')
        parser.add_argument('-d', '--description', dest='description', action='store', type=str, default=None, help='the detailed description of the resource.')
        parser.add_argument('-S', '--s2-class', dest='s2_class', action='store', type=int, default=None, help='valid values includes 0, 1.')
        return

    @classmethod
    def build_directive(cls, options):
        for key in ['vxnet', 'service_type']:
            if not hasattr(options, key):
                print 'error: [%s] should be specified.' % key
                return None

        directive = {'vxnet': options.vxnet, 'service_type': options.service_type, 
           's2_server_name': options.s2_server_name, 
           's2_server_type': options.s2_server_type, 
           'private_ip': options.private_ip, 
           'description': options.description, 
           's2_class': options.s2_class}
        return directive