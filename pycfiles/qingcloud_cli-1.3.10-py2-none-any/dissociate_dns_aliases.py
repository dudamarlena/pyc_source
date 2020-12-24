# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/dns_alias/dissociate_dns_aliases.py
# Compiled at: 2015-09-04 04:28:20
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class DissociateDNSAliasesAction(BaseAction):
    action = 'DissociateDNSAliases'
    command = 'dissociate-dns-aliases'
    usage = '%(prog)s -d "dns_alias_id, ..." [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-d', '--dns_aliases', dest='dns_aliases', action='store', type=str, default='', help='the comma separated IDs of dns alias you want to dissociate.')

    @classmethod
    def build_directive(cls, options):
        dns_aliases = explode_array(options.dns_aliases)
        if not dns_aliases:
            return None
        else:
            return {'dns_aliases': dns_aliases}