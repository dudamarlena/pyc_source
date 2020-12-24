# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/sg/delete_security_groups.py
# Compiled at: 2015-05-26 14:08:44
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DeleteSecurityGroupsAction(BaseAction):
    action = 'DeleteSecurityGroups'
    command = 'delete-security-groups'
    usage = '%(prog)s -s "security_group_id, ..." [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--security_groups', dest='security_groups', action='store', type=str, default='', help='the IDs of the security groups you want to delete.')

    @classmethod
    def build_directive(cls, options):
        security_groups = explode_array(options.security_groups)
        if not security_groups:
            print '[security_groups] should be specified.'
            return None
        else:
            return {'security_groups': security_groups}