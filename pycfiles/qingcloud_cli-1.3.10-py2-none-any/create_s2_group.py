# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/create_s2_group.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.iaas_client.actions.base import BaseAction

class CreateS2GroupAction(BaseAction):
    action = 'CreateS2Group'
    command = 'create-s2-group'
    usage = '%(prog)s -T <group_type> [-n <group_name> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-T', '--group-type', dest='group_type', action='store', type=str, default=None, help='valid values is NFS_GROUP or SMB_GROUP.')
        parser.add_argument('-n', '--group-name', dest='group_name', action='store', type=str, default=None, help='the name of group.')
        parser.add_argument('-s', '--s2-accounts', dest='s2_accounts', action='store', type=str, default=None, help='the IDs of s2 accounts.')
        parser.add_argument('-d', '--description', dest='description', action='store', type=str, default=None, help='the detailed description of the resource.')
        return

    @classmethod
    def build_directive(cls, options):
        for key in ['group_type']:
            if not hasattr(options, key):
                print 'error: [%s] should be specified.' % key
                return None

        directive = {'group_type': options.group_type, 'group_name': options.group_name, 
           's2_accounts': options.s2_accounts, 
           'description': options.description}
        return directive