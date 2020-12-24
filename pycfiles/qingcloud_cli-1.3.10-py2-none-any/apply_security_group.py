# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/sg/apply_security_group.py
# Compiled at: 2017-09-21 02:37:46
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ApplySecurityGroupAction(BaseAction):
    action = 'ApplySecurityGroup'
    command = 'apply-security-group'
    usage = '%(prog)s -s <security_group_id> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--security_group_id', dest='security_group_id', action='store', type=str, default='', help='ID of the security group you want to apply to instances.')
        parser.add_argument('-i', '--instances', dest='instances', action='store', type=str, default='', help='the comma-separated IDs of instances you want to apply the security group to.')
        parser.add_argument('-u', '--target-user', dest='target_user', action='store', type=str, default=None, help='the ID of user who will own this resource.')
        return

    @classmethod
    def build_directive(cls, options):
        required_params = {'security_group_id': options.security_group_id}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        return {'security_group': options.security_group_id, 
           'instances': explode_array(options.instances), 
           'target_user': options.target_user}