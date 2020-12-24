# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pygnet/client.py
# Compiled at: 2007-07-08 08:09:35
import atexit
from collections import deque
from twisted.internet import protocol, reactor
import pygame
from protocol import GameProtocol
inbox = deque()
running = False

class GameClient(protocol.ClientFactory):

    def clientConnectionFailed(self, connector, reason):
        pass

    def clientConnectionLost(self, connector, reason):
        pass

    def new_connection(self, client):
        inbox.append(('new_connection', dict(connection=client)))

    def lost_connection(self, client):
        inbox.append(('lost_connection', dict(connection=client)))

    def receive_object(self, client, obj):
        inbox.append(('recv', dict(connection=client, obj=obj)))


def shutdown():
    global running
    if running:
        reactor.stop()
        reactor.iterate(0.1)
    running = False


def init(host, port):
    global running
    atexit.register(shutdown)
    factory = GameClient()
    factory.protocol = GameProtocol
    reactor.connectTCP(host, port, factory)
    reactor.startRunning(False)
    reactor.iterate(0.01)
    running = True


def poll():
    reactor.iterate(0.1)


def get_events():
    while True:
        try:
            event = inbox.pop()
        except IndexError:
            return
        else:
            yield event