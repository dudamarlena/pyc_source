# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pygnet/server.py
# Compiled at: 2007-07-08 08:09:35
from twisted.internet import protocol, reactor
from protocol import GameProtocol

class GameServer(protocol.ServerFactory):

    def new_connection(self, client):
        pass

    def lost_connection(self, client):
        pass

    def recieve_object(self, client, obj):
        pass

    def send_object(self, client, obj):
        client.send_object(obj)


call_later = reactor.callLater

def run_server(ServerClass, port):
    factory = ServerClass()
    factory.protocol = GameProtocol
    reactor.listenTCP(port, factory)
    reactor.run()


if __name__ == '__main__':
    run_server(GameServer, 1979)