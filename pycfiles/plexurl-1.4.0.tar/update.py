# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/plexshell/commands/update.py
# Compiled at: 2011-09-15 10:10:11
from plexshell.commands import PlexCmd

class UpdateCmd(PlexCmd):
    """ Mixin that provides a command to trigger the auto-updating process """

    def do_update(self, s):
        print 'Updating plugins'
        get(self.conn, '/system/appstore/updates/install', 'Updating failed: ')

    def help_update(self):
        print 'Intitiate the the Plex AppStore auto-update process'