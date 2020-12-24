# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/dns_alias/associate_dns_alias.py
# Compiled at: 2015-09-04 04:05:33
from qingcloud.cli.iaas_client.actions.base import BaseAction

class AssociateDNSAliasAction(BaseAction):
    action = 'AssociateDNSAlias'
    command = 'associate-dns-alias'
    usage = '%(prog)s -p <prefix> -r <resource_id> [options] [-f <conf_file>]'
    description = 'Associate DNS alias to resource'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-p', '--prefix', dest='prefix', action='store', type=str, default='', help='the prefix of the dns alias.')
        parser.add_argument('-r', '--resource', dest='resource', action='store', type=str, default='', help='the ID of resource you want to associate.')

    @classmethod
    def build_directive(cls, options):
        if not options.prefix or not options.resource:
            print 'error: [prefix] and [resource] should be specified'
            return None
        else:
            return {'prefix': options.prefix, 
               'resource': options.resource}