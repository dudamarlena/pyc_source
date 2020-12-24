# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/disable_s2_shared_targets.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DisableS2SharedTargetsAction(BaseAction):
    action = 'DisableS2SharedTargets'
    command = 'disable-s2-shared-targets'
    usage = '%(prog)s -s <shared_targets>  [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--shared-targets', dest='shared_targets', action='store', type=str, default=None, help='the IDs of shared targets you want to disable.')
        return

    @classmethod
    def build_directive(cls, options):
        for key in ['shared_targets']:
            if not hasattr(options, key):
                print 'error: [%s] should be specified.' % key
                return None

        directive = {'shared_targets': explode_array(options.shared_targets)}
        return directive