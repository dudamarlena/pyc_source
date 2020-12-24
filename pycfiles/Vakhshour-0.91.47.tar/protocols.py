# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/Vakhshour/vakhshour/protocols.py
# Compiled at: 2012-09-04 10:58:06
import json
from zope.interface import implements
from twisted.internet import protocol, reactor
from twisted.protocols.amp import AMP
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.defer import succeed
from twisted.web.iweb import IBodyProducer
from base import VObject
from commands import Event

class EventProtocol(AMP, VObject):

    def __init__(self, publisher, *args, **kwargs):
        self.publisher = publisher
        super(EventProtocol, self).__init__(*args, **kwargs)

    @Event.responder
    def event_responser(self, name, sender, kwargs):
        params = {'name': name, 'sender': sender}
        params.update(kwargs)
        self.logger.info('PARAMS: %s' % unicode(params))
        self.publisher.send(**params)
        return {'status': 0}


class EventFactory(protocol.Factory):
    """
    Event transport factory. reponsible for received Events.
    """
    protocol = EventProtocol

    def __init__(self, sender_factory):
        self.sender = sender_factory

    def buildProtocol(self, addr):
        p = self.protocol(self.sender)
        return p


class EventPublisher(protocol.Protocol):
    """
    This protocol is in charge of publishing valid events to the
    Vakhshour clients.
    """

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        """
        Each time a client connect to publisher the EventPublisher
        instance for that client stores in a set object in
        EventPublisherFactory.
        """
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        pass


class EventPublisherFactory(protocol.Factory, VObject):
    protocol = EventPublisher

    def __init__(self, webapps):
        self.clients = set()
        self.webapps = webapps

    def buildProtocol(self, addr):
        p = self.protocol(self)
        return p

    def send(self, **kwargs):
        for c in self.clients:
            data = json.dumps(kwargs)
            self.logger.info('Publish: %s' % data)
            c.transport.write(data)

        if self.webapps:
            agent = Agent(reactor)
            for app in self.webapps:
                protocol, domain = self._parse_url(app)
                if protocol == 'http':
                    url = str('http://%s/event/' % domain.rstrip('/'))
                    body = self.JsonProducer(kwargs, self.Encoder())
                elif protocol == 'https':
                    url = str('https://%s/event/' % domain.rstrip('/'))
                    encoder = self.Encoder('SSL', self.webapps[app])
                    body = self.JsonProducer(kwargs, encoder)
                elif protocol == 'rsa':
                    url = str('http://%s/event/' % domain.rstrip('/'))
                    encoder = self.Encoder('RSA', self.webapps[app])
                    body = self.JsonProducer(kwargs, encoder)
                d = agent.request('GET', url, Headers({'User-Agent': ['Vakhshour']}), body)
                d.addCallback(self._response)

    def _parse_url(self, url):
        try:
            protocol, domain = url.split('://')
            return (protocol, domain)
        except ValueError:
            raise ValueError("'%s' is not well formatted." % url)

    def _response(self, ignore):
        pass

    class Encoder(VObject):

        def __init__(self, codec=None, pub_key=None):
            super(EventPublisherFactory.Encoder, self).__init__()
            self.codec = codec
            self.key = pub_key
            self.logger.info(self.codec)

        def encode(self, data):
            if not self.codec:
                return data
            if self.codec.lower() == 'ssl':
                raise self.NotImplemented('This method not implemented.')
            else:
                if self.codec.lower() == 'rsa':
                    from Crypto.PublicKey import RSA
                    key = RSA.importKey(file(self.key).read())
                    data = key.encrypt(data, 7)[0]
                    return data
                raise ValueError("Unknown codec '%s'" % self.codec)

    class JsonProducer(object):
        implements(IBodyProducer)

        def __init__(self, body, encoder=None):
            self.body = json.dumps(body)
            self.encoder = encoder
            self.encrypted_data = self.encoder.encode(self.body)
            self.length = len(self.encrypted_data)

        def startProducing(self, consumer):
            consumer.write(self.encrypted_data)
            return succeed(None)

        def pauseProducing(self):
            pass

        def stopProducing(self):
            pass


class Subscribe(protocol.Protocol, VObject):
    """
    Event Subscribe Protocol.

    Main protocol to receiving events
    """

    def dataReceived(self, data):
        """
        This function called when a an event received.
        """
        try:
            event = json.loads(data)
        except:
            raise

        print '>>> ', event

    class EventNotSent(Exception):
        pass


class SubscribeFactory(protocol.ReconnectingClientFactory):
    """
    Event transport factory. reponsible for received Events.
    """
    protocol = Subscribe

    def buildProtocol(self, addr):
        p = self.protocol()
        return p