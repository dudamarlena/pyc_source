# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/sg/modify_security_group_ipset_attributes.py
# Compiled at: 2017-07-19 00:52:36
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifySecurityGroupIPSetAttributesAction(BaseAction):
    action = 'ModifySecurityGroupIPSetAttributes'
    command = 'modify-security-group-ipset-attributes'
    usage = '%(prog)s -s <security_group_ipset_id> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--security_group_ipset_id', dest='security_group_ipset_id', action='store', type=str, default='', help='the ID of the security group ipset you want to update its content.')
        parser.add_argument('-N', '--security_group_ipset_name', dest='security_group_ipset_name', action='store', type=str, default=None, help='the new name for the security group ipset you want to update.')
        parser.add_argument('-D', '--description', dest='description', action='store', type=str, default=None, help='the detailed description of the resource')
        parser.add_argument('-V', '--val', dest='val', action='store', type=str, default=None, help='the val of the resource, such as 192.168.1.0/24 or 10000-15000')
        return

    @classmethod
    def build_directive(cls, options):
        required_params = {'security_group_ipset_id': options.security_group_ipset_id}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'param [%s] should be specified' % param
                return

        return {'security_group_ipset': options.security_group_ipset_id, 
           'security_group_ipset_name': options.security_group_ipset_name, 
           'val': options.val, 
           'description': options.description}