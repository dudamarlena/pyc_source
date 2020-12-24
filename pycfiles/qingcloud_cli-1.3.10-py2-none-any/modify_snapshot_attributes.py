# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/snapshot/modify_snapshot_attributes.py
# Compiled at: 2015-05-26 14:09:10
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifySnapshotAttributesAction(BaseAction):
    action = 'ModifySnapshotAttributes'
    command = 'modify-snapshot-attributes'
    usage = '%(prog)s -s snapshot_id [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--snapshot', dest='snapshot', action='store', type=str, default='', help='the id of the snapshot whose attributes you want to modify.')
        parser.add_argument('-N', '--name', dest='snapshot_name', action='store', type=str, default=None, help='specify the new snapshot name.')
        parser.add_argument('-D', '--description', dest='description', action='store', type=str, default=None, help='the detailed description of the resource.')
        return

    @classmethod
    def build_directive(cls, options):
        if not options.snapshot:
            print 'error: [snapshot] should be specified'
            return None
        else:
            return {'snapshot': options.snapshot, 
               'snapshot_name': options.snapshot_name, 
               'description': options.description}