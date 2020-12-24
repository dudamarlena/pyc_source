# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/drones/honeypot/capabilities/vnc.py
# Compiled at: 2016-11-12 07:38:04
import socket, random, logging, SocketServer
from beeswarm.drones.honeypot.capabilities.handlerbase import HandlerBase
from beeswarm.shared.vnc_constants import *
logger = logging.getLogger(__name__)

class BaitVncHandler(SocketServer.StreamRequestHandler):
    """
        Handler of VNC Connections. This is a rather primitive state machine.
    """

    def __init__(self, request, client_address, server, session):
        self.session = session
        SocketServer.StreamRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        self.request.send(RFB_VERSION)
        client_version = self.request.recv(1024)
        if client_version == RFB_VERSION:
            self.security_handshake()
        else:
            self.finish()

    def security_handshake(self):
        self.request.send(SUPPORTED_AUTH_METHODS)
        sec_method = self.request.recv(1024)
        if sec_method == VNC_AUTH:
            self.do_vnc_authentication()
        else:
            self.finish()

    def do_vnc_authentication(self):
        challenge = get_random_challenge()
        self.request.send(challenge)
        client_response_ = self.request.recv(1024)
        self.session.try_auth('des_challenge', challenge=challenge, response=client_response_)
        if self.session.authenticated:
            self.request.send(AUTH_SUCCESSFUL)
        else:
            self.request.send(AUTH_FAILED)
        self.finish()


class Vnc(HandlerBase):

    def __init__(self, options, work_dir):
        super(Vnc, self).__init__(options, work_dir)
        self._options = options

    def handle_session(self, gsocket, address):
        session = self.create_session(address)
        try:
            try:
                BaitVncHandler(gsocket, address, None, session)
            except socket.error as err:
                logger.debug(('Unexpected end of VNC session: {0}, errno: {1}. ({2})').format(err, err.errno, session.id))

        finally:
            self.close_session(session)

        return


def get_random_challenge():
    challenge = []
    for i in range(0, 16):
        temp = random.randint(0, 255)
        challenge.append(chr(temp))

    return ('').join(challenge)