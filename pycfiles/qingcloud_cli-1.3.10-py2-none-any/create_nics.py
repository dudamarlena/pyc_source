# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/nic/create_nics.py
# Compiled at: 2017-05-07 03:25:42
from qingcloud.cli.iaas_client.actions.base import BaseAction
from qingcloud.cli.misc.utils import explode_array

class CreateNicsAction(BaseAction):
    action = 'CreateNics'
    command = 'create-nics'
    usage = '%(prog)s --vxnet <vxnet> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-x', '--vxnet', dest='vxnet', action='store', type=str, default=None, help='the ID of vxnet.')
        parser.add_argument('-N', '--nic-name', dest='nic_name', action='store', type=str, default=None, help='the name of nic.')
        parser.add_argument('-p', '--private-ips', dest='private_ips', action='store', type=str, default=None, help='the private ip of nics. ')
        parser.add_argument('-c', '--count', dest='count', action='store', type=int, default=1, help='the number of nics to create.')
        return

    @classmethod
    def build_directive(cls, options):
        required_params = {'vxnet': options.vxnet}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        return {'vxnet': options.vxnet, 
           'count': options.count, 
           'nic_name': options.nic_name, 
           'private_ips': explode_array(options.private_ips)}