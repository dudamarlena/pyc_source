# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/eip/change_eips_bandwidth.py
# Compiled at: 2015-05-26 14:04:31
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ChangeEipsBandwidthAction(BaseAction):
    action = 'ChangeEipsBandwidth'
    command = 'change-eips-bandwidth'
    usage = '%(prog)s -e "eip_id, ..." -b <bandwidth> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-e', '--eips', dest='eips', action='store', type=str, default='', help='the comma separated IDs of eips you want to change their bandwidth.')
        parser.add_argument('-b', '--bandwidth', dest='bandwidth', action='store', type=int, default=0, help='new bandwidth, in MB.')
        return parser

    @classmethod
    def build_directive(cls, options):
        eips = explode_array(options.eips)
        bandwidth = options.bandwidth
        if not eips or not bandwidth:
            print 'error: [eips] and [bandwidth] should be specified'
            return None
        else:
            return {'eips': eips, 
               'bandwidth': bandwidth}