# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/s2/describe_s2_servers.py
# Compiled at: 2017-07-19 01:59:02
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeS2ServersAction(BaseAction):
    action = 'DescribeS2Servers'
    command = 'describe-s2-servers'
    usage = '%(prog)s [-s <s2_servers> ...] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--s2-servers', dest='s2_servers', action='store', type=str, default=None, help='the IDs of s2 server you want to describe.')
        parser.add_argument('-T', '--service-types', dest='service_types', action='store', type=str, default=None, help="the type of service, valid value is 'vsan' or 'vnas'.")
        parser.add_argument('-S', '--status', dest='status', action='store', type=str, default=None, help='valid values include pending, active, poweroffed, suspended, deleted, ceased.')
        parser.add_argument('-w', '--search-word', dest='search_word', action='store', type=str, default=None, help='you may use this field to search from id, name and description.')
        parser.add_argument('-t', '--tags', dest='tags', action='store', type=str, default=None, help='the array of IDs of tags.')
        parser.add_argument('-v', '--verbose', dest='verbose', action='store', type=int, default=None, help='the number to specify the verbose level, larger the number, the more detailed information will be returned.')
        return

    @classmethod
    def build_directive(cls, options):
        directive = {'s2_servers': explode_array(options.s2_servers), 
           'service_types': explode_array(options.service_types), 
           'status': explode_array(options.status), 
           'search_word': options.search_word, 
           'tags': explode_array(options.tags), 
           'verbose': options.verbose}
        return directive