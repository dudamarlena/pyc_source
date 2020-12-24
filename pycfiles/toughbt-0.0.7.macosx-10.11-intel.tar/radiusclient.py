# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/toughbt/radiusclient.py
# Compiled at: 2016-03-17 09:34:46
from twisted.python import log
from twisted.internet import protocol
from twisted.internet import reactor, defer
from txradius.radius import packet
from txradius import message
import six, time

class RadiusClient(protocol.DatagramProtocol):

    def __init__(self, secret, dictionary, server, authport=1812, acctport=1813, debug=False, stat_counter=None):
        self.dict = dictionary
        self.secret = six.b(secret)
        self.server = server
        self.authport = authport
        self.acctport = acctport
        self.debug = debug
        self.stat_counter = stat_counter
        reactor.listenUDP(0, self)

    def close(self):
        if self.transport is not None:
            self.transport.stopListening()
            self.transport = None
        return

    def sendAuth(self, **kwargs):
        User_Password = kwargs.pop('User-Password', None)
        CHAP_Password = kwargs.pop('CHAP-Password', None)
        CHAP_Challenge = kwargs.get('CHAP-Challenge')
        request = message.AuthMessage(dict=self.dict, secret=self.secret, **kwargs)
        if User_Password:
            request['User-Password'] = request.PwCrypt(User_Password)
        if CHAP_Password:
            if CHAP_Challenge:
                request['CHAP-Challenge'] = CHAP_Challenge
            request['CHAP-Password'] = CHAP_Password
        if self.debug:
            log.msg('Send radius Auth Request to (%s:%s): %s' % (self.server, self.authport, request.format_str()))
        self.transport.write(request.RequestPacket(), (self.server, self.authport))
        self.stat_counter.requests += 1
        return

    def datagramReceived(self, datagram, (host, port)):
        try:
            response = packet.Packet(packet=datagram, dict=self.dict, secret=self.secret)
            self.stat_counter.plus(response)
            if self.debug:
                log.msg('Received Radius Response from %s: %s' % ((host, port), message.format_packet_str(response)))
        except Exception as err:
            log.err('Invalid Response packet from %s: %s' % ((host, port), str(err)))
            self.stat_counter.error(err)