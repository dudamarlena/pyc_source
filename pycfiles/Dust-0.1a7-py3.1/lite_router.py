# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/server/lite_router.py
# Compiled at: 2010-06-01 14:15:05
from dust.extensions.multiplex.lite_multiplex_socket import *
from dust.crypto.keys import KeyManager
from dust.core.util import getPublicIP
from dust.server.services import services
print('services:', services)

class LitePacketRouter:

    def __init__(self, v6, port, keys):
        self.host = getPublicIP(v6)
        self.port = port
        msock = lite_multiplex_socket(keys)
        msock.bind((self.host, self.port))
        while 1:
            msg, addr, service = msock.mrecvfrom(1024)
            if msg and addr and service:
                handler = services[service]
                handler(msg, addr)
                continue