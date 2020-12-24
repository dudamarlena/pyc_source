# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aioyoyo\oyoyo\services.py
# Compiled at: 2017-01-05 03:30:40
# Size of source mod 2**32: 2177 bytes
import sys
from .helpers import msg
_nickservfuncs = ('register', 'group', 'glist', 'identify', 'access', 'drop', 'recover',
                  'release', 'sendpass', 'ghost', 'alist', 'info', 'list', 'logout',
                  'status', 'update')
_nickservsetfuncs = ('display', 'password', 'language', 'url', 'email', 'icq', 'greet',
                     'kill', 'secure', 'private', 'hide', 'msg', 'autoop')
_chanservfuncs = ('register', 'identify', 'sop', 'aop', 'hop', 'vop', 'access', 'levels',
                  'akick', 'drop', 'sendpass', 'ban', 'unban', 'clear', 'owner',
                  'deowner', 'protect', 'deprotect', 'op', 'deop', 'halfop', 'dehalfop',
                  'voice', 'devoice', 'getkey', 'invite', 'kick', 'list', 'logout',
                  'topic', 'info', 'appendtopic', 'enforce')
_chanservsetfuncs = ('founder', 'successor', 'password', 'desc', 'url', 'email', 'entrymsg',
                     'bantype', 'mlock', 'keeptopic', 'opnotice', 'peace', 'private',
                     'restricted', 'secure', 'secureops', 'securefounder', 'signkick',
                     'topiclock', 'xop')

def _addServ(serv, funcs, prefix=''):

    def simplecmd(cmd_name):
        if prefix:
            cmd_name = prefix.upper() + ' ' + cmd_name

        def f(cli, *args):
            print(cmd_name, ' '.join(args))

        return f

    for t in funcs:
        setattr(serv, t, simplecmd(t.upper()))


class NickServ(object):

    def __init__(self, nick='NickServ'):
        self.name = nick
        _addServ(self, _nickservfuncs)
        _addServ(self, _nickservsetfuncs, 'set')


class ChanServ(object):

    def __init__(self, nick='ChanServ'):
        self.name = nick
        _addServ(self, _chanservfuncs)
        _addServ(self, _chanservsetfuncs, 'set')