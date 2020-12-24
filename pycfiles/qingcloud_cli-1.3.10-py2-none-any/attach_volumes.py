# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/volume/attach_volumes.py
# Compiled at: 2015-05-26 14:09:21
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class AttachVolumesAction(BaseAction):
    action = 'AttachVolumes'
    command = 'attach-volumes'
    usage = '%(prog)s -i <instance_id> -v "volume_id,..." [-f <conf_file>]'
    description = 'Attach one or more volumes to instance'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-i', '--instance', dest='instance', action='store', type=str, default='', help='the ID of instance the volumes will be attached to.')
        parser.add_argument('-v', '--volumes', dest='volumes', action='store', type=str, default='', help='the comma separated IDs of volumes you want to attach.')

    @classmethod
    def build_directive(cls, options):
        required_params = {'instance': options.instance, 
           'volumes': options.volumes}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        return {'volumes': explode_array(options.volumes), 
           'instance': options.instance}