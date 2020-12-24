# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/sg/create_security_group_ipset.py
# Compiled at: 2017-09-21 02:37:46
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateSecurityGroupIPSetAction(BaseAction):
    action = 'CreateSecurityGroupIPSet'
    command = 'create-security-group-ipset'
    usage = '%(prog)s --security_group_ipset_name <security_group_ipset_name> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-N', '--security_group_ipset_name', dest='security_group_ipset_name', action='store', type=str, default='', help='short name for the security group ipset you want to create.')
        parser.add_argument('-T', '--ipset_type', dest='ipset_type', action='store', type=int, default=0, help='type of the security group ipset you want to create, 0 is IP, 1 is port.')
        parser.add_argument('-V', '--val', dest='val', action='store', type=str, default='', help='value of this ipset, such as: 192.168.1.0/24 or 10000-15000.')
        parser.add_argument('-u', '--target-user', dest='target_user', action='store', type=str, default=None, help='the ID of user who will own this resource.')
        return

    @classmethod
    def build_directive(cls, options):
        required_params = {'security_group_ipset_name': options.security_group_ipset_name, 
           'ipset_type': options.ipset_type, 
           'val': options.val}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'param [%s] should be specified' % param
                return

        if options.target_user:
            required_params['target_user'] = options.target_user
        return required_params