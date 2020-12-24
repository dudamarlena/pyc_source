# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrana/plugins/pidginstatus.py
# Compiled at: 2011-07-09 22:56:18
import dbus
from feather import Plugin

class PidginStatus(Plugin):
    listeners = set(['songstart', 'songpause', 'songresume'])
    messengers = set()

    def songstart(self, payload):
        parts = payload.split('/')
        artist = parts[(-3)]
        album = parts[(-2)]
        song = parts[(-1)]
        self.song_msg = '%s (%s): %s' % (artist, album, song)
        self.update_status(self.song_msg)

    def songpause(self, payload=None):
        self.update_status('Paused')

    def songresume(self, payload=None):
        self.update_status(self.song_msg)

    def update_status(self, msg):
        bus = dbus.SessionBus()
        if 'im.pidgin.purple.PurpleService' in bus.list_names():
            purple = bus.get_object('im.pidgin.purple.PurpleService', '/im/pidgin/purple/PurpleObject', 'im.pidgin.purple.PurpleInterface')
            current = purple.PurpleSavedstatusGetType(purple.PurpleSavedstatusGetCurrent())
            status = purple.PurpleSavedstatusNew('', current)
            purple.PurpleSavedstatusSetMessage(status, msg)
            purple.PurpleSavedstatusActivate(status)