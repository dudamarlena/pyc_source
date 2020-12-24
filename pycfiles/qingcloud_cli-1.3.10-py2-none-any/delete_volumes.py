# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/volume/delete_volumes.py
# Compiled at: 2015-05-26 14:09:23
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteVolumesAction(BaseAction):
    action = 'DeleteVolumes'
    command = 'delete-volumes'
    usage = '%(prog)s -v "volume_id,..." [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-v', '--volumes', dest='volumes', action='store', type=str, default='', help='the comma separated IDs of volumes you want to delete.')

    @classmethod
    def build_directive(cls, options):
        if not options.volumes:
            print 'error: [volumes] should be specified'
            return None
        else:
            return {'volumes': explode_array(options.volumes)}