# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aioyoyo\oyoyo\examplebot.py
# Compiled at: 2017-03-02 00:29:21
# Size of source mod 2**32: 1009 bytes
"""Example bot for aioyoyo that responds to !say"""
import logging, re
from .client import IRCClient
from . import helpers
from .cmdhandler import DefaultCommandHandler
HOST = 'irc.freenode.net'
PORT = 6667
NICK = 'aioyoyo-example'
CHANNEL = '#aioyoyo-test'

class MyHandler(DefaultCommandHandler):

    def privmsg(self, nick, chan, msg):
        msg = msg.decode()
        match = re.match('\\!say (.*)', msg)
        if match:
            to_say = match.group(1).strip()
            print('Saying, "%s"' % to_say)
            helpers.msg(self.client, chan, to_say)


def connect_cb(cli):
    helpers.join(cli, CHANNEL)


def main():
    logging.basicConfig(level=(logging.DEBUG))
    cli = IRCClient(MyHandler, host=HOST, port=PORT, nick=NICK, connect_cb=connect_cb)
    conn = cli.connect()
    while True:
        next(conn)


if __name__ == '__main__':
    main()