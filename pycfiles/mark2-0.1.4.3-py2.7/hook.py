# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/events/hook.py
# Compiled at: 2013-08-16 22:15:55
from . import Event

class Hook(Event):
    name = Event.Arg()
    is_command = Event.Arg()
    args = Event.Arg()
    line = Event.Arg()

    def setup(self):
        if not self.name:
            if self.line:
                t = self.line.split(' ', 1)
                self.name = t[0][1:]
                self.is_command = True
                if len(t) == 2:
                    self.args = t[1]

    def prefilter(self, name, public=False, doc=None):
        if name != self.name:
            return False
        if self.is_command and not public:
            return False
        return True