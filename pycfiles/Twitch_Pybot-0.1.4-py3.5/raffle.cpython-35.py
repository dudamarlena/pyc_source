# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybot/features/raffle.py
# Compiled at: 2016-07-13 16:56:07
# Size of source mod 2**32: 1910 bytes
import threading, time, random
from pybot.pybotextra import *

class Raffle:

    def __init__(self, conn, data, params):
        self.conn = conn
        self.data = globals.data
        self.users = []
        self.params = {'name': '', 'trigger': '!joinraffle', 'cost': 0, 'minpoints': 0}
        conn.addHook(self.hook)
        for pair in params:
            try:
                split = pair.split(':')
                self.setParam(split[0], split[1])
            except:
                nothing = 0

        conn.msg('%s has begun! to join say %s in chat' % (self.params['name'], self.params['trigger']))

    def chooseWinner(self):
        winner = self.users[random.randint(0, len(self.users) - 1)]
        self.conn.msg('The winner is: ' + winner)
        return winner

    def setParam(self, param, value):
        self.params[param] = value

    def hook(self, con, msg, event):
        if event == 'user_privmsg':
            name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
            text = msg.split('PRIVMSG')[1].replace('%s :' % con.channel, '')
            if checkIfCommand(text, self.params['trigger']):
                try:
                    userPoints = self.data.points[name]
                except:
                    userPoints = 0
                    self.data.points[name] = 0

                if userPoints >= int(self.params['minpoints']) and userPoints >= int(self.params['cost']) and name not in self.users:
                    self.users.append(name)
                    self.data.points[name] -= int(self.params['cost'])
                    self.data.save()
                    con.msg(name + ' has entered the raffle!')

    def __del__(self):
        self.conn.removeHook(self.hook)