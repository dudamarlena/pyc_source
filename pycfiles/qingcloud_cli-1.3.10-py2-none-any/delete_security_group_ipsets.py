# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/sg/delete_security_group_ipsets.py
# Compiled at: 2017-07-19 00:52:36
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteSecurityGroupIPSetsAction(BaseAction):
    action = 'DeleteSecurityGroupIPSets'
    command = 'delete-security-group-ipsets'
    usage = '%(prog)s -s "security_group_ipset_id, ..." [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--security_group_ipsets', dest='security_group_ipsets', action='store', type=str, default='', help='the IDs of the security group ipsets you want to delete.')

    @classmethod
    def build_directive(cls, options):
        security_group_ipsets = explode_array(options.security_group_ipsets)
        if not security_group_ipsets:
            print '[security_group_ipsets] should be specified.'
            return None
        else:
            return {'security_group_ipsets': security_group_ipsets}