# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/volume/create_volumes.py
# Compiled at: 2017-05-07 02:03:05
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateVolumesAction(BaseAction):
    action = 'CreateVolumes'
    command = 'create-volumes'
    usage = '%(prog)s --size <volume_size> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--size', dest='size', action='store', type=int, default=None, help='the size of each volume. Unit is GB.')
        parser.add_argument('-t', '--type', dest='volume_type', action='store', type=int, default=0, help='the type of volumes:\n                "0" means high performance volume.\n                "1" means high capacity volume in pek1, gd1, ap1.\n                "2" means high capacity volume in pek2.\n                ')
        parser.add_argument('-c', '--count', dest='count', action='store', type=int, default=1, help='the number of volumes to create.')
        parser.add_argument('-N', '--volume_name', dest='volume_name', action='store', type=str, default='', help='short name of volume')
        parser.add_argument('--target-user', dest='target_user', action='store', type=str, default=None, help='ID of user who will own this resource, should be one of your sub-account.')
        return

    @classmethod
    def build_directive(cls, options):
        required_params = {'size': options.size}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        return {'size': options.size, 
           'count': options.count, 
           'volume_name': options.volume_name, 
           'volume_type': options.volume_type, 
           'target_user': options.target_user}