# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybot/pybot_main.py
# Compiled at: 2016-07-13 16:56:07
# Size of source mod 2**32: 4770 bytes
import sys, threading, json, os
os.chdir(os.path.dirname(__file__) or '.')
from pybot.data import *
from pybot.irc import irc
from pybot.pybotextra import *
from pybot.features.raffle import Raffle
from pybot.features.commands import Commands
from pybot.features.points import Points
from pybot.features.linkgrabber import Linkgrabber
from pybot.features.quotes import Quotes
from pybot.web import pybot_web
import pybot.globals as globals
PYBOT_VERSION = {'status': 'BETA', 'version': 0, 'build': 121}
PWD = os.getcwd()

def main():
    settings = globals.settings
    pybotPrint('PYBOT %s VERSION %s BUILD %s' % (PYBOT_VERSION['status'], PYBOT_VERSION['version'], PYBOT_VERSION['build']), 'usermsg')
    if len(json.loads(settings.config['filters']['activeFilters'])) <= 0:
        pybotPrint('[pybot.main] Running with no filters', 'log')
    con = irc(feed)
    globals.con = con
    cmds = Commands(con)
    if toBool(settings.config['points']['enabled']):
        points = Points(con, con.chatters, settings, data)
    if toBool(settings.config['features']['linkgrabber']):
        linkgrabber = Linkgrabber(con)
    if toBool(settings.config['features']['quotes']):
        quotes = Quotes(con)
    threading.Thread(target=con.connect).start()
    if toBool(settings.config['web']['enabled']):
        web = pybot_web.pybot_web(con)
        threading.Thread(target=web.startWebService).start()
    while con.isClosed() == False:
        if con.connected:
            inp = input('')
            if inp:
                con.msg(inp)

    pybotPrint('[PYBOT] connection ended', 'log')
    exit()


def feed(con, msg, event):
    if event == 'server_cantchannel' or event == 'server_lost':
        pybotPrint('Lost connection')
        con.retry()
    else:
        if event == 'nick_taken':
            pybotPrint('Nick has been taken!')
            con.retry()
        else:
            if event == 'user_join':
                name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
                if name != con.nick:
                    joins = getUserData(name)
                    setUserData(name, joins + 1)
            else:
                if event == 'user_privmsg':
                    name = msg.replace(':', '').split('!')[0].replace('\n\r', '')
                    text = msg.split('PRIVMSG')[1].replace('%s :' % con.channel, '')
                    if con.isMod(name) == False and name != 'jtv':
                        con.filter(name, text)
                    if checkIfCommand(text, '!raffle'):
                        if toBool(globals.settings.config['features']['raffle']):
                            texsplit = text.replace('!raffle', '').split(' ')
                            raffle = Raffle(con, con.data, texsplit)
                            globals.data.raffles.append(raffle)
                    else:
                        if checkIfCommand(text, '!leave'):
                            if con.isMod(name):
                                con.msg('Bye!')
                                con.close()
                            else:
                                con.msg('%s, you do not have access to this command.' % name)
                        else:
                            if checkIfCommand(text, '!permit'):
                                cmd_args = text.split(' ')
                                if con.isMod(name):
                                    con.msg('%s can post a link' % cmd_args[2])
                                    con.addMode(cmd_args[2], '+permit')
                            else:
                                con.msg('%s, you do not have access to this command.' % name)
                    if con.isMod(name):
                        pybotPrint('%s : %s' % (name, text), 'usermsg-mod')
                    else:
                        pybotPrint('%s : %s' % (name, text), 'usermsg')
                elif event == 'user_mode':
                    name = msg.split(' ')[4].replace('\n\r', '')
                    pybotPrint('%s is mode %s' % (name, con.getMode(name)))


def setUserData(user, data):
    return 0


def getUserData(user):
    return 0


if __name__ == '__main__':
    main()