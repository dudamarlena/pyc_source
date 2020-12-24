# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/snapshot/capture_instance_from_snapshot.py
# Compiled at: 2015-05-26 14:09:04
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CaptureInstanceFromSnapshotAction(BaseAction):
    action = 'CaptureInstanceFromSnapshot'
    command = 'capture-instance-from-snapshot'
    usage = '%(prog)s -s <snapshot> -n <image-name> [-f <conf_file>]'
    description = 'capture instance image from snapshot.'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--snapshot', dest='snapshot', action='store', type=str, default='', help='the ID of snapshot you want to capture as image.')
        parser.add_argument('-N', '--image-name', dest='image_name', action='store', type=str, default='', help='the name of image.')

    @classmethod
    def build_directive(cls, options):
        required_params = {'snapshot': options.snapshot}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        return {'snapshot': options.snapshot, 
           'image_name': options.image_name}