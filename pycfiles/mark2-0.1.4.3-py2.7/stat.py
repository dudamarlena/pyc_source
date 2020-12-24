# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/events/stat.py
# Compiled at: 2013-08-16 22:15:55
from . import Event

class StatEvent(Event):
    source = Event.Arg()


class StatPlayerCount(StatEvent):
    players_current = Event.Arg(required=True)
    players_max = Event.Arg(required=True)


class StatPlayers(StatEvent):
    players = Event.Arg(required=True)


class StatProcess(StatEvent):
    cpu = Event.Arg(required=True)
    memory = Event.Arg(required=True)