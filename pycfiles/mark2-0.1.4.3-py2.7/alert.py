# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/plugins/alert.py
# Compiled at: 2013-08-16 22:15:55
import os, random
from mk2.plugins import Plugin

class Alert(Plugin):
    interval = Plugin.Property(default=200)
    command = Plugin.Property(default='say {message}')
    path = Plugin.Property(default='alerts.txt')
    messages = []

    def setup(self):
        if self.path and os.path.exists(self.path):
            f = open(self.path, 'r')
            for l in f:
                l = l.strip()
                if l:
                    self.messages.append(l)

            f.close()

    def server_started(self, event):
        if self.messages:
            self.repeating_task(self.repeater, self.interval)

    def repeater(self, event):
        self.send_format(self.command, message=random.choice(self.messages))