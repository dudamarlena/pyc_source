# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/detach_from_s2_shared_target.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DetachFromS2SharedTargetAction(BaseAction):
    action = 'DetachFromS2SharedTarget'
    command = 'detach-from-s2-shared-target'
    usage = '%(prog)s -s <shared_target> -v <volumes>  [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--shared-target', dest='shared_target', action='store', type=str, default=None, help='the ID of shared target.')
        parser.add_argument('-v', '--volumes', dest='volumes', action='store', type=str, default=None, help='the IDs of volumes.')
        return

    @classmethod
    def build_directive(cls, options):
        for key in ['shared_target', 'volumes']:
            if not hasattr(options, key):
                print 'error: [%s] should be specified.' % key
                return None

        directive = {'shared_target': options.shared_target, 'volumes': explode_array(options.volumes)}
        return directive