# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/dissociate_s2_account_group.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DissociateS2AccountGroupAction(BaseAction):
    action = 'DissociateS2AccountGroup'
    command = 'dissociate-s2-account-group'
    usage = '%(prog)s -s <s2_groups> -S <s2_accounts>  [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--s2-groups', dest='s2_groups', action='store', type=str, default=None, help='the IDs of groups.')
        parser.add_argument('-S', '--s2-accounts', dest='s2_accounts', action='store', type=str, default=None, help='the IDs of accounts.')
        return

    @classmethod
    def build_directive(cls, options):
        for key in ['s2_groups', 's2_accounts']:
            if not hasattr(options, key):
                print 'error: [%s] should be specified.' % key
                return None

        directive = {'s2_groups': explode_array(options.s2_groups), 's2_accounts': explode_array(options.s2_accounts)}
        return directive