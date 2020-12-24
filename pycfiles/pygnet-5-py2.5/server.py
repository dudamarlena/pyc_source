# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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