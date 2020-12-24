# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/create_s2_account.py
# Compiled at: 2017-07-19 02:11:32
import json
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateS2AccountAction(BaseAction):
    action = 'CreateS2Account'
    command = 'create-s2-account'
    usage = '%(prog)s -T <account_type> [-n <account_name> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-T', '--account-type', dest='account_type', action='store', type=str, default=None, help='valid values is NFS or SMB.')
        parser.add_argument('-n', '--account-name', dest='account_name', action='store', type=str, default=None, help='the name of account.')
        parser.add_argument('-s', '--smb-name', dest='smb_name', action='store', type=str, default=None, help='the user name of smb.')
        parser.add_argument('-S', '--smb-passwd', dest='smb_passwd', action='store', type=str, default=None, help='the password of smb.')
        parser.add_argument('-N', '--nfs-ipaddr', dest='nfs_ipaddr', action='store', type=str, default=None, help='ip address available in NFS.')
        parser.add_argument('-g', '--s2-groups', dest='s2_groups', action='store', type=str, default=None, help='the JSON form of groups. e.g. \'[{"group_id":"s2g-xxxx", "rw_flag": "rw"}]\'')
        parser.add_argument('-o', '--opt-parameters', dest='opt_parameters', action='store', type=str, default=None, help='options parameters for NFS.')
        parser.add_argument('-d', '--description', dest='description', action='store', type=str, default=None, help='the detailed description of the resource.')
        return

    @classmethod
    def build_directive(cls, options):
        for key in ['account_type']:
            if not hasattr(options, key):
                print 'error: [%s] should be specified.' % key
                return None

        directive = {'account_type': options.account_type, 'account_name': options.account_name, 
           'smb_name': options.smb_name, 
           'smb_passwd': options.smb_passwd, 
           'nfs_ipaddr': options.nfs_ipaddr, 
           's2_groups': json.loads(options.s2_groups), 
           'opt_parameters': options.opt_parameters, 
           'description': options.description}
        return directive