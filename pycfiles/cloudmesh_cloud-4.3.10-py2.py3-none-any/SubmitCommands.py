# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/SubmitCommands.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
from cloudmesh_client.shell.command import PluginCommand
from cloudmesh_client.shell.command import command

class SubmitCommands(PluginCommand):
    topics = {'submit': 'system'}

    def __init__(self, context):
        super(self.__class__, self).__init__()
        self.context = context
        if self.context.debug:
            print('init SubmitCommands')

    @command
    def do_submit(self, args, arguments):
        """
        ::

            Usage:
                submit ARGUMENTS...

            We do not yet know what this command will do ;-)

            Arguments:
                ARGUMENTS       The arguments passed to nova

            Options:
                -v              verbose mode

        """
        return 'Not implemented yet.'