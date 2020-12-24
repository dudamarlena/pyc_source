# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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