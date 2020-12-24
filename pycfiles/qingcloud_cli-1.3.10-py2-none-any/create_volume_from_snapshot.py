# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/snapshot/create_volume_from_snapshot.py
# Compiled at: 2015-05-26 14:09:06
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateVolumeFromSnapshotAction(BaseAction):
    action = 'CreateVolumeFromSnapshot'
    command = 'create-volume-from-snapshot'
    usage = '%(prog)s -s "snapshot_id" -n <name> [-f <conf_file>]'
    description = 'Create volume from snapshot.'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--snapshot', dest='snapshot', action='store', type=str, default='', help='the ID of snapshot you want to create volume from it.')
        parser.add_argument('-N', '--volume-name', dest='volume_name', action='store', type=str, default='', help='the name of new volume.')

    @classmethod
    def build_directive(cls, options):
        if not options.snapshot:
            print 'error: [snapshots] should be specified'
            return None
        else:
            return {'snapshot': options.snapshot, 
               'volume_name': options.volume_name}