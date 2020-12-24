# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bezel/networking/client.py
# Compiled at: 2009-02-25 04:20:27
import socket, simplejson

class GameEngineProxy(object):
    """
    A class which provides the same attributes of the server's game
    engine, on the fly.
    """

    def __init__(self, client):
        self.__client = client

    def __getattribute__(self, name):
        try:
            return super(GameEngineProxy, self).__getattribute__(name)
        except AttributeError:

            def fn(*args, **kwargs):
                return self.__client.request(name, *args, **kwargs)

            setattr(self, name, fn)
            return fn


class JSONGameClient(object):

    def __init__(self, host, port):
        self.server_address = (
         host, port)
        self.socket = socket.socket()
        self.socket.connect(self.server_address)
        self.engine = GameEngineProxy(self)
        self.buffer = ''

    def __del__(self):
        self.socket.close()

    def send(self, data):
        self.socket.send(data + '\n')

    def read(self):
        position = self.buffer.find('\n')
        while position == -1:
            self.buffer += self.socket.recv(1024)
            position = self.buffer.find('\n')

        result = self.buffer[:position + 1].rstrip('\r\n')
        self.buffer = self.buffer[position + 1:]
        return result

    def request(self, message, *args, **kwargs):
        args = simplejson.dumps(args)
        kwargs = simplejson.dumps(kwargs)
        data = ('\n').join([message, args, kwargs])
        self.send(data)
        response = self.read()
        return simplejson.loads(response)