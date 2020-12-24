# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/shell/plugins/ServerCommand.py
# Compiled at: 2017-04-23 10:30:41
import os
from cloudmesh_client.shell.command import command
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand

class ServerCommand(PluginCommand, CloudPluginCommand):
    topics = {'server': 'cloud'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print 'init command server'

    @command
    def do_server(self, args, arguments):
        """
        Usage:
            server

        Options:
          -h --help
          -v       verbose mode

        Description:
          Starts up a REST service and a WEB GUI so one can browse the data in an
          existing cloudmesh database.

          The location of the database is supposed to be in

            ~/.cloud,esh/cloudmesh.db

        """
        from sandman import app
        from sandman.model import activate
        filename = ('sqlite:///{}').format(Config.path_expand(os.path.join('~', '.cloudmesh', 'cloudmesh.db')))
        print ('database: {}').format(filename)
        app.config['SQLALCHEMY_DATABASE_URI'] = filename
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        activate()
        app.run()