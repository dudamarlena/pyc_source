# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/sg/create_security_group.py
# Compiled at: 2017-09-21 02:37:46
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateSecurityGroupAction(BaseAction):
    action = 'CreateSecurityGroup'
    command = 'create-security-group'
    usage = '%(prog)s --group_name <group_name> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-N', '--security_group_name', dest='security_group_name', action='store', type=str, default='', help='short name for the security group you want to create.')
        parser.add_argument('-u', '--target-user', dest='target_user', action='store', type=str, default=None, help='the ID of user who will own this resource.')
        return

    @classmethod
    def build_directive(cls, options):
        required_params = {'security_group_name': options.security_group_name}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'param [%s] should be specified' % param
                return

        return {'security_group_name': options.security_group_name, 'target_user': options.target_user}