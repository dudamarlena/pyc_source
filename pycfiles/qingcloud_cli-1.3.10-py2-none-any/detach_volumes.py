# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/volume/detach_volumes.py
# Compiled at: 2015-05-26 14:09:26
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DetachVolumesAction(BaseAction):
    action = 'DetachVolumes'
    command = 'detach-volumes'
    usage = '%(prog)s -i <instance_id> -v "volume_id,..." [-f <conf_file>]'
    description = 'Detach one or more volumes from instance.'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-i', '--instance', dest='instance', action='store', type=str, default='', help='the comma separated IDs of volumes you want to describe.')
        parser.add_argument('-v', '--volumes', dest='volumes', action='store', type=str, default='', help='the ID of instance the volumes will be detached from.')

    @classmethod
    def build_directive(cls, options):
        required_params = {'volumes': options.volumes, 
           'instance': options.instance}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        return {'volumes': explode_array(options.volumes), 
           'instance': options.instance}