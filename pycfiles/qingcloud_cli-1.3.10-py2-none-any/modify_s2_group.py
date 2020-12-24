# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/modify_s2_group.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class ModifyS2GroupAction(BaseAction):
    action = 'ModifyS2Group'
    command = 'modify-s2-group'
    usage = '%(prog)s -s <s2_group> [-n <group_name> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--s2-group', dest='s2_group', action='store', type=str, default=None, help='the ID of group.')
        parser.add_argument('-n', '--group-name', dest='group_name', action='store', type=str, default=None, help='the name of group.')
        parser.add_argument('-S', '--s2-accounts', dest='s2_accounts', action='store', type=str, default=None, help='the IDs of accounts.')
        parser.add_argument('-d', '--description', dest='description', action='store', type=str, default=None, help='the new value of description.')
        return

    @classmethod
    def build_directive(cls, options):
        for key in ['s2_group']:
            if not hasattr(options, key):
                print 'error: [%s] should be specified.' % key
                return None

        directive = {'s2_group': options.s2_group, 'group_name': options.group_name, 
           's2_accounts': explode_array(options.s2_accounts), 
           'description': options.description}
        return directive