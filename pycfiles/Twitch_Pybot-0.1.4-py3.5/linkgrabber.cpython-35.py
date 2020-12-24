# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybot/features/linkgrabber.py
# Compiled at: 2016-07-13 16:56:07
# Size of source mod 2**32: 2251 bytes
from pybot.pybotextra import *
import pybot.globals as globals
from pybot.data import *
import re

class Linkgrabber:

    def __init__(self, conn):
        self.conn = conn
        self.active = False
        self.webRegex = re.compile('((ftp|http|https):\\/\\/)?([a-zA-Z0-9]+(\\.[a-zA-Z0-9]+)+.*)', re.IGNORECASE)
        conn.addHook(self.hook)

    def hook(self, con, msg, event):
        if event == 'user_privmsg':
            name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
            text = msg.split('PRIVMSG')[1].replace('%s :' % con.channel, '')
            if checkIfCommand(text, '!linkgrabber'):
                if con.isMod(name):
                    if self.active:
                        self.active = False
                        con.msg('Link grabber has been disabled!')
                    elif toBool(globals.settings.config['features']['linkgrabber']):
                        self.active = True
                        con.msg('Link grabber has been enabled! post your links!')
                else:
                    con.msg('%s, you do not have access to this command.' % name)
        else:
            if checkIfCommand(text, '!linkban'):
                cmd_args = text.split(' ')
                if con.isMod(name):
                    self.linkBan(cmd_args[2])
            else:
                con.msg('%s, you do not have access to this command.' % name)
        if self.active == True and name not in globals.data.linkbanned and self.webRegex.search(text) is not None and globals.settings.config['linkgrabber']['filter'] in text:
            globals.data.links[name] = text
            globals.data.save()
            con.msg(name + ', your link has been grabbed.')

    def linkBan(self, name):
        if name not in globals.data.linkbanned:
            globals.data.linkbanned.append(name)
            globals.data.save()
        else:
            globals.data.linkbanned.remove(name)
            globals.data.save()