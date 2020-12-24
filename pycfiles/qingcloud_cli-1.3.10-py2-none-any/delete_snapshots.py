# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/snapshot/delete_snapshots.py
# Compiled at: 2015-05-26 14:09:07
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteSnapshotsAction(BaseAction):
    action = 'DeleteSnapshots'
    command = 'delete-snapshots'
    usage = '%(prog)s -s "snapshot_id,..." [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--snapshots', dest='snapshots', action='store', type=str, default='', help='the comma separated IDs of snapshots you want to delete.')

    @classmethod
    def build_directive(cls, options):
        if not options.snapshots:
            print 'error: [snapshots] should be specified'
            return None
        else:
            return {'snapshots': explode_array(options.snapshots)}