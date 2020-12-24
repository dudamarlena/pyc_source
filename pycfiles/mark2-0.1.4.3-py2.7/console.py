# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/events/console.py
# Compiled at: 2013-08-16 22:15:55
from . import Event, get_timestamp
from ..shared import console_repr

class Console(Event):
    contains = ('line', 'time', 'user', 'source', 'kind', 'data', 'level')
    requires = ('line', )
    line = Event.Arg(required=True)
    kind = Event.Arg()
    time = Event.Arg()
    user = Event.Arg(default='')
    source = Event.Arg(default='mark2')
    data = Event.Arg()
    level = Event.Arg()

    def setup(self):
        if not self.time:
            self.time = get_timestamp(self.time)
        if not self.data:
            self.data = self.line

    def value(self):
        return console_repr(self)