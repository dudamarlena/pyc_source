# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/plugins/su.py
# Compiled at: 2013-08-16 22:15:55
from mk2.plugins import Plugin
from mk2.events import UserInput

class Su(Plugin):
    command = Plugin.Property(default='sudo -su {user} -- {command}')
    mode = Plugin.Property(default='include')
    proc = Plugin.Property(default='ban;unban')

    def setup(self):
        self.register(self.uinput, UserInput)

    def uinput(self, event):
        handled = False
        for p in self.proc.split(';'):
            if event.line.startswith(p):
                handled = True
                break

        if (self.mode == 'exclude') ^ handled:
            event.line = self.command.format(user=event.user, command=event.line)