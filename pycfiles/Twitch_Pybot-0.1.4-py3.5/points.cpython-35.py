# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybot/features/points.py
# Compiled at: 2016-07-13 16:56:07
# Size of source mod 2**32: 1413 bytes
import threading, time
from pybot.pybotextra import *
import pybot.globals as globals

class Points:

    def __init__(self, con, chatters, settings, data):
        self.con = con
        self.chatters = chatters
        self.settings = settings
        self.data = data
        con.addHook(self.hook)
        threading.Thread(target=self.pointsCheck).start()

    def pointsCheck(self):
        if globals.data.points:
            time.sleep(60 * float(globals.settings.config['points']['interval_in_minutes']))
            for user in self.chatters.mods:
                globals.data.addPoints(user, float(globals.settings.config['points']['points_to_append']))

            for user in self.chatters.viewers:
                globals.data.addPoints(user, float(globals.settings.config['points']['points_to_append']))

            globals.data.save()
            self.pointsCheck()

    def hook(self, con, msg, event):
        if event == 'user_privmsg':
            name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
            text = msg.split('PRIVMSG')[1].replace('%s :' % con.channel, '')
            if checkIfCommand(text, '!points'):
                try:
                    con.msg(name + ', you have ' + str(con.data.points[name]) + ' points.')
                except:
                    con.msg(name + ', you have 0 points.')