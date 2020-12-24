# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/server/router.py
# Compiled at: 2010-06-01 17:02:18
from dust.extensions.multiplex.multiplex_socket import *
from dust.crypto.keys import KeyManager
from dust.core.util import getPublicIP
from dust.util.safethread import SafeThread
from dust.server.activeServices import activeServices
print('services:', activeServices)

class PacketRouter:

    def __init__(self, v6, port, keys, passwd):
        self.host = getPublicIP(v6)
        self.port = port
        self.keys = keys
        self.passwd = passwd
        self.msock = multiplex_socket(self.keys)
        self.msock.bind((self.host, self.port))
        self.ui = None
        for service in activeServices.values():
            service.setRouter(self)

        return

    def getService(self, name):
        return activeServices[name]

    def connect(self, dest, outport):
        self.msock.connect((dest, outport))

    def connectToService(self, service):
        self.msock.connectToService(service)

    def setUI(self, ui):
        self.ui = ui
        for service in activeServices.values():
            service.setUI(ui)

    def start(self):
        self.thread = SafeThread(target=self.run)
        self.thread.start()

    def run(self):
        while 1:
            msg, addr, service = self.msock.mrecvfrom(1024)
            if msg and addr and service:
                handler = activeServices[service]
                handler.handle(self.msock, msg, addr)
                continue

    def send(self, msg, service=None):
        if service:
            self.msock.msend(msg.encode('ascii'), service=service)
        else:
            self.msock.msend(msg.encode('ascii'))

    def sendto(self, msg, addr, service=None):
        print('router.sendto ' + str(addr))
        if service:
            self.msock.msendto(msg.encode('ascii'), addr, service=service)
        else:
            self.msock.msendto(msg.encode('ascii'), addr)