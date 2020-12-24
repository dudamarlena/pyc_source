# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pywebqq/client.py
# Compiled at: 2014-07-25 04:09:55
from redis import Redis
import struct, readline, re, colorama
colorama.init()
from colorama import Fore
MESSAGE = 1
SHAKEMESSAGE = 2
GRPMESSAGE = 3
LOGOUTMESSAGE = 4
IMAGEMESSAGE = 5

class Chat(object):

    def __init__(self):
        self.lastfriend = ''
        self.conn = Redis(host='localhost', db=10)
        self.runflag = True

    def executecmd(self, cmd, param):
        if cmd == 'shake':
            self.sendto(SHAKEMESSAGE, param, '')
            self.lastfriend = param
        elif cmd == 'to':
            self.lastfriend = param
        elif cmd == 'online':
            guyscount = 0
            for guy in self.conn.hkeys('onlineguys'):
                if self.conn.hget('onlineguys', guy) != 'offline':
                    print guy
                    guyscount += 1

            print '在线好友 %s%d%s' % (Fore.GREEN, guyscount, Fore.RESET)
        elif cmd == 'stat':
            guy = self.conn.hget('onlineguys', param)
            if guy:
                print Fore.YELLOW + guy + Fore.RESET
        elif cmd == 'image':
            if self.lastfriend and param:
                self.sendto(IMAGEMESSAGE, self.lastfriend, param)
            else:
                print Fore.RED + '请先选择朋友或输入图像路径' + Fore.RESET
        elif cmd == 'brodcast':
            for guy in self.conn.lrange('onlinefriends', 0, -1):
                to = guy[0:guy.find('-')]
                self.sendto(MESSAGE, to, param)

        elif cmd == 'quit':
            self.runflag = False
            self.sendto(LOGOUTMESSAGE, None, None)
        elif cmd == 'exit':
            self.runflag = False
        else:
            print Fore.RED + ':quit ' + Fore.RESET + 'exit client'
            print Fore.RED + ':shake FRIEND ' + Fore.RESET + 'send shake message to friend'
            print Fore.RED + ':online ' + Fore.RESET + 'show all online friends'
            print Fore.RED + ':stat FRIEND' + Fore.RESET + ' show friends status'
        return

    def parsecmd(self, message):
        cmdpattern = re.compile('^(:)(\\w*)\\s?(.*)$')
        msgpattern = re.compile('^(\\|)?(.*)$')
        cmdmatch, msgmatch = cmdpattern.match(message), msgpattern.match(message)
        if cmdmatch:
            _, cmd, param = cmdmatch.groups()
            self.executecmd(cmd, param)
        elif msgmatch:
            prefix, remaintext = msgmatch.groups()
            if prefix == '|':
                tokens = remaintext.split()
                to, body = tokens[0], ('').join(tokens[1:])
            else:
                to, body = self.lastfriend, remaintext
            if body == '':
                return
            msgtype = GRPMESSAGE if to.find('_') > -1 else MESSAGE
            self.sendto(msgtype, to, body)

    def sendto(self, msgtype, to, message):
        bytemsg = ''
        if msgtype == LOGOUTMESSAGE:
            bytemsg = struct.pack('i', 4)
        else:
            if not to:
                return
            tolen, messagelen = len(to), len(message)
            if msgtype in (MESSAGE, GRPMESSAGE, IMAGEMESSAGE):
                bytemsg = struct.pack('iii%ss%ss' % (tolen, messagelen), msgtype, tolen, messagelen, to, message)
            elif msgtype == SHAKEMESSAGE:
                bytemsg = struct.pack('ii%ss' % tolen, msgtype, tolen, to)
        self.conn.lpush('messagepool', bytemsg)

    def getfriends(self):
        self.friendsinfo = self.conn.lrange('friends', 0, -1)
        self.groupsinfo = self.conn.lrange('groups', 0, -1)
        self.friendsinfo.extend(self.groupsinfo)
        return self

    def completer(self, prefix, index):
        matches = [ friend for friend in self.friendsinfo if friend.startswith(prefix) ]
        try:
            return matches[index]
        except IndexError:
            pass

    def chat(self):
        readline.parse_and_bind('tab:complete')
        readline.set_completer(self.completer)
        while self.runflag:
            message = raw_input('=>%s: ' % self.lastfriend)
            self.parsecmd(message)


def main():
    Chat().getfriends().chat()