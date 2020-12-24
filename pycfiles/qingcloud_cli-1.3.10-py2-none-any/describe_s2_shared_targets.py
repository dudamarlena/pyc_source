# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/describe_s2_shared_targets.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeS2SharedTargetsAction(BaseAction):
    action = 'DescribeS2SharedTargets'
    command = 'describe-s2-shared-targets'
    usage = '%(prog)s [-s <shared_targets> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--shared-targets', dest='shared_targets', action='store', type=str, default=None, help='the IDs of shared targets.')
        parser.add_argument('-T', '--target-types', dest='target_types', action='store', type=str, default=None, help="valid values includes 'ISCSI', 'FCoE','NFS' and 'SMB'.")
        parser.add_argument('-S', '--s2-server-id', dest='s2_server_id', action='store', type=str, default=None, help='the ID of s2 server.')
        parser.add_argument('-n', '--export-name', dest='export_name', action='store', type=str, default=None, help='the name of shared target.')
        parser.add_argument('-w', '--search-word', dest='search_word', action='store', type=str, default=None, help='you may use this field to search from export_name or description.')
        parser.add_argument('-v', '--verbose', dest='verbose', action='store', type=int, default=None, help='the number to specify the verbose level, larger the number, the more detailed information will be returned.')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'shared_targets': explode_array(options.shared_targets), 
           'target_types': explode_array(options.target_types), 
           's2_server_id': options.s2_server_id, 
           'export_name': options.export_name, 
           'search_word': options.search_word, 
           'verbose': options.verbose}
        return directive