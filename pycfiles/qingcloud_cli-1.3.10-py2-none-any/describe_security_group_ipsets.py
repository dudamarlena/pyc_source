# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/sg/describe_security_group_ipsets.py
# Compiled at: 2017-07-19 00:52:36
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeSecurityGroupIPSetsAction(BaseAction):
    action = 'DescribeSecurityGroupIPSets'
    command = 'describe-security-group-ipsets'
    usage = '%(prog)s [-s "security_group_ipset_id, ..."] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--security_group_ipsets', dest='security_group_ipsets', action='store', type=str, default='', help='the comma separated IDs of security_group_ipsets you want to list. ')
        parser.add_argument('-W', '--security_group_ipset_name', dest='security_group_ipset_name', action='store', type=str, default='', help='search by name')
        parser.add_argument('-T', '--ipset_type', dest='ipset_type', action='store', type=int, default=0, help='the type of ipsets, 0 is IP, 1is port')
        parser.add_argument('-V', '--verbose', dest='verbose', action='store', type=int, default=0, help='the number to specify the verbose level, larger the number, the more detailed information will be returned.')

    @classmethod
    def build_directive(cls, options):
        return {'security_group_ipsets': explode_array(options.security_group_ipsets), 
           'security_group_ipset_name': options.security_group_ipset_name, 
           'ipset_type': options.ipset_type, 
           'verbose': options.verbose, 
           'offset': options.offset, 
           'limit': options.limit}