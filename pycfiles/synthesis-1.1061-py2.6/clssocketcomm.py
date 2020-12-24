# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/clssocketcomm.py
# Compiled at: 2010-12-12 22:28:56
import sys
from time import sleep

class serviceController:

    def __init__(self, bServer=True):
        import socket
        self.host = 'localhost'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bServer = bServer
        if bServer:
            self.serverPort = 8081
            self.clientPort = 8082
        else:
            self.serverPort = 8082
            self.clientPort = 8081
        self.s.bind(('', self.serverPort))

    def send(self, msg):
        self.s.sendto(msg, (self.host, self.clientPort))

    def getStatus(self, msg):
        self.send(msg)
        self.s.settimeout(5)
        try:
            (data, addr) = self.s.recvfrom(1024)
        except:
            return 'Synthesis is not Running...'

        if data == 'synthesis:running':
            return 'Synthesis is Running...'

    def listen(self):
        if self.bServer:
            port = self.serverPort
        else:
            port = self.clientPort
        print 'waiting on port', port
        while 1:
            (data, addr) = self.s.recvfrom(1024)
            print 'Received: ', data, 'from:', addr
            if data == 'synthesis:status':
                self.send('synthesis:running')
            if data == 'synthesis:stop':
                print 'stopping hard'
                sys.exit(0)