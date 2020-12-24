# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/describe_s2_groups.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeS2GroupsAction(BaseAction):
    action = 'DescribeS2Groups'
    command = 'describe-s2-groups'
    usage = '%(prog)s [-s <s2_groups> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--s2-groups', dest='s2_groups', action='store', type=str, default=None, help='the IDs of s2 groups.')
        parser.add_argument('-T', '--group-types', dest='group_types', action='store', type=str, default=None, help='valid values is NFS_GROUP or SMB_GROUP.')
        parser.add_argument('-n', '--group-name', dest='group_name', action='store', type=str, default=None, help='the name of group.')
        parser.add_argument('-S', '--search-word', dest='search_word', action='store', type=str, default=None, help='you may use this field to search from id or name.')
        parser.add_argument('-v', '--verbose', dest='verbose', action='store', type=int, default=None, help='the number to specify the verbose level, larger the number, the more detailed information will be returned.')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'s2_groups': explode_array(options.s2_groups), 
           'group_types': explode_array(options.group_types), 
           'group_name': options.group_name, 
           'search_word': options.search_word, 
           'verbose': options.verbose}
        return directive