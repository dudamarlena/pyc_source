# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/events/player.py
# Compiled at: 2013-08-16 22:15:55
from . import Event

class PlayerEvent(Event):

    def setup(s):
        s.username = s.username.encode('ascii')


class PlayerJoin(PlayerEvent):
    username = Event.Arg(required=True)
    ip = Event.Arg(required=True)


class PlayerQuit(PlayerEvent):
    username = Event.Arg(required=True)
    reason = Event.Arg(required=True)


class PlayerChat(PlayerEvent):
    username = Event.Arg(required=True)
    message = Event.Arg(required=True)


class PlayerDeath(PlayerEvent):
    text = Event.Arg()
    username = Event.Arg(required=True)
    cause = Event.Arg(required=True)
    killer = Event.Arg()
    weapon = Event.Arg()
    format = Event.Arg(default='{username} died')

    def get_text(self, **kw):
        d = dict((k, getattr(self, k)) for k in ('username', 'killer', 'weapon'))
        d.update(kw)
        return self.format.format(**d)

    def setup(self):
        self.text = self.get_text()