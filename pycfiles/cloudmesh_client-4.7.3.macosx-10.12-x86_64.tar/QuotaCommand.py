# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/QuotaCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.quota import Quota
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand

class QuotaCommand(PluginCommand, CloudPluginCommand):
    topics = {'quota': 'cloud'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command quota')

    @command
    def do_quota(self, args, arguments):
        """
        ::

            Usage:
                quota list [--cloud=CLOUD] [--tenant=TENANT] [--format=FORMAT]

                Prints quota limit on a current project/tenant

            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name
               --tenant=TENANT  the tenant id

            Examples:
                cm quota list
                cm quota list --cloud=india --format=csv

        """
        if arguments['list']:
            cloud = arguments['--cloud'] or Default.cloud
            if not cloud:
                Console.error("Default cloud doesn't exist")
                return
            tenant = arguments['--tenant']
            output_format = arguments['--format']
            list_quotas = Quota.list(cloud, tenant, output=output_format)
            Console.msg(list_quotas)
            return