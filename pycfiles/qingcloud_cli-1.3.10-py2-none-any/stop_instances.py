# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/instance/stop_instances.py
# Compiled at: 2015-05-26 14:05:46
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class StopInstancesAction(BaseAction):
    action = 'StopInstances'
    command = 'stop-instances'
    usage = '%(prog)s -i "instance_id,..." [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-i', '--instances', dest='instances', action='store', type=str, default='', help='the comma separated IDs of instances you want to stop.')
        parser.add_argument('-F', '--force', action='store_const', const=1, dest='force', help='forcibly shutdown.')
        return parser

    @classmethod
    def build_directive(cls, options):
        instances = explode_array(options.instances)
        if not instances:
            print 'error: [instances] should be specified'
            return None
        else:
            directive = {'instances': instances}
            if options.force:
                directive.update({'force': options.force})
            return directive