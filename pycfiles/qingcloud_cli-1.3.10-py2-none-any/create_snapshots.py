# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/snapshot/create_snapshots.py
# Compiled at: 2015-05-26 14:09:05
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateSnapshotsAction(BaseAction):
    action = 'CreateSnapshots'
    command = 'create-snapshots'
    usage = '%(prog)s -r <resources> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--resources', dest='resources', action='store', type=str, default=None, help='the IDs of resources you want to create snapshot from')
        parser.add_argument('-F', '--is-full', dest='is_full', action='store', type=int, default=0, help='1 means create full snapshot, 0 means determined by the system.')
        parser.add_argument('-N', '--name', dest='snapshot_name', action='store', type=str, default='', help='short name of snapshot')
        return

    @classmethod
    def build_directive(cls, options):
        required_params = {'resources': options.resources}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        return {'resources': explode_array(options.resources), 
           'is_full': options.is_full, 
           'snapshot_name': options.snapshot_name}