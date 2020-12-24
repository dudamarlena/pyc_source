# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/FlavorCommand.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.cloud.flavor import Flavor
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default

class FlavorCommand(PluginCommand, CloudPluginCommand):
    topics = {'flavor': 'cloud'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print('init command flavor')

    @command
    def do_flavor(self, args, arguments):
        """
        ::

            Usage:
                flavor refresh [--cloud=CLOUD] [-v]
                flavor list [ID] [--cloud=CLOUD] [--format=FORMAT] [--refresh] [-v]

                This lists out the flavors present for a cloud

            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name
               --refresh        refreshes the data before displaying it
                                from the cloud

            Examples:
                cm flavor refresh
                cm flavor list
                cm flavor list --format=csv
                cm flavor show 58c9552c-8d93-42c0-9dea-5f48d90a3188 --refresh

        """
        cloud = arguments['--cloud'] or Default.cloud
        if cloud is None:
            Console.error("Default cloud doesn't exist")
            return
        else:
            if arguments['-v']:
                print(('Cloud: {}').format(cloud))
            if arguments['refresh'] or Default.refresh:
                msg = ('Refresh flavor for cloud {:}.').format(cloud)
                if Flavor.refresh(cloud):
                    Console.ok(('{:} ok').format(msg))
                else:
                    Console.error(('{:} failed').format(msg))
                    return ''
            if arguments['list']:
                id = arguments['ID']
                live = arguments['--refresh']
                output_format = arguments['--format']
                counter = 0
                result = None
                while counter < 2:
                    if id is None:
                        result = Flavor.list(cloud, output_format)
                    else:
                        result = Flavor.details(cloud, id, live, output_format)
                    if counter == 0 and result is None:
                        if not Flavor.refresh(cloud):
                            msg = ('Refresh flavor for cloud {:}.').format(cloud)
                            Console.error(('{:} failed.').format(msg))
                    counter += 1

                if result is None:
                    Console.error('No flavor(s) found. Failed.')
                else:
                    print(result)
                return ''
            return