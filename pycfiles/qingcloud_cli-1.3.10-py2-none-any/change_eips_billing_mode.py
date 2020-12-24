# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/eip/change_eips_billing_mode.py
# Compiled at: 2015-05-26 14:04:35
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ChangeEipsBillingModeAction(BaseAction):
    action = 'ChangeEipsBillingMode'
    command = 'change-eips-billing-mode'
    usage = '%(prog)s -e "eip_id, ..." -b <billing-mode> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-e', '--eips', dest='eips', action='store', type=str, default='', help='the comma separated IDs of eips you want to change their billing mode.')
        parser.add_argument('-b', '--billing-mode', dest='billing_mode', action='store', type=str, default='', help='new billing mode, "traffic" or "bandwidth".')
        return parser

    @classmethod
    def build_directive(cls, options):
        eips = explode_array(options.eips)
        billing_mode = options.billing_mode
        if not eips or not billing_mode:
            print 'error: [eips] and [billing-mode] should be specified'
            return None
        else:
            return {'eips': eips, 
               'billing_mode': billing_mode}