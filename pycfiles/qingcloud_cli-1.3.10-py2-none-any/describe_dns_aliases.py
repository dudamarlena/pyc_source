# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/dns_alias/describe_dns_aliases.py
# Compiled at: 2015-09-04 05:30:19
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DescribeDNSAliasesAction(BaseAction):
    action = 'DescribeDNSAliases'
    command = 'describe-dns-aliases'
    usage = '%(prog)s [-d "dns-aliases, ..."] [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-d', '--dns_aliases', dest='dns_aliases', action='store', type=str, default='', help='the comma separated IDs of dns_aliases you want to describe. ')
        parser.add_argument('-r', '--resource_id', dest='resource_id', action='store', type=str, default=None, help='filter dns aliases by resource id')
        return

    @classmethod
    def build_directive(cls, options):
        return {'dns_aliases': explode_array(options.dns_aliases), 
           'resource_id': options.resource_id, 
           'offset': options.offset, 
           'limit': options.limit}