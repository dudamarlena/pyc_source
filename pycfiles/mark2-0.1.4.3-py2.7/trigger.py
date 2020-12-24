# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/plugins/trigger.py
# Compiled at: 2013-08-16 22:15:55
import os, re
from mk2.plugins import Plugin
from mk2.events import ServerOutput

class Trigger(Plugin):
    command = Plugin.Property(default='msg {user} {message}')
    path = Plugin.Property(default='triggers.txt')
    triggers = {}

    def setup(self):
        if self.path and os.path.exists(self.path):
            f = open(self.path, 'r')
            for l in f:
                m = re.match('^\\!?([^,]+),(.+)$', l)
                if m:
                    a, b = m.groups()
                    c = self.triggers.get(a, [])
                    c.append(b)
                    self.triggers[a] = c

            f.close()
            if self.triggers:
                self.register(self.trigger, ServerOutput, pattern='<([A-Za-z0-9_]{1,16})> \\!(\\w+)')

    def trigger(self, event):
        user, trigger = event.match.groups()
        if trigger in self.triggers:
            for line in self.triggers[trigger]:
                self.send(self.command.format(user=user, message=line))