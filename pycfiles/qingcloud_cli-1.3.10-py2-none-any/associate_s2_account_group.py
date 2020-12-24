# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/associate_s2_account_group.py
# Compiled at: 2017-07-19 02:11:32
import json
from qingcloud.cli.iaas_client.actions.base import BaseAction

class AssociateS2AccountGroupAction(BaseAction):
    action = 'AssociateS2AccountGroup'
    command = 'associate-s2-account-group'
    usage = '%(prog)s -s <s2_group> -S <s2_accounts>  [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--s2-group', dest='s2_group', action='store', type=str, default=None, help='the ID of group.')
        parser.add_argument('-S', '--s2-accounts', dest='s2_accounts', action='store', type=str, default=None, help='the JSON form of accounts. e.g. \'[{"account_id": "s2a-xxxx", "rw_flag": "rw"}]\'')
        return

    @classmethod
    def build_directive(cls, options):
        for key in ['s2_group', 's2_accounts']:
            if not hasattr(options, key):
                print 'error: [%s] should be specified.' % key
                return None

        directive = {'s2_group': options.s2_group, 's2_accounts': json.loads(options.s2_accounts)}
        return directive