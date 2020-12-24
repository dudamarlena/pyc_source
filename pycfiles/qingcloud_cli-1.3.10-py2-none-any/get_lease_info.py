# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/billing/get_lease_info.py
# Compiled at: 2017-11-28 04:06:50
from qingcloud.cli.iaas_client.actions.base import BaseAction

class GetLeaseInfoAction(BaseAction):
    action = 'GetLeaseInfo'
    command = 'get-lease-info'
    usage = '%(prog)s -r <resource> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-r', '--resource', dest='resource', action='store', type=str, default='', help='the ID of resource which lease info you want to get.')
        parser.add_argument('-u', '--user', dest='user', action='store', type=str, default=None, help='the ID of user.')
        return

    @classmethod
    def build_directive(cls, options):
        if options.resource == '':
            print 'error: resource should be specified.'
            return None
        else:
            directive = {'resource': options.resource, 
               'user': options.user}
            return directive