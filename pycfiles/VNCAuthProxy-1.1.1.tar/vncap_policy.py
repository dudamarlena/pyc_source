# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kennric/Projects/twisted_vncauthproxy/twisted/plugins/vncap_policy.py
# Compiled at: 2014-05-21 16:51:12
from twisted.application.internet import TCPServer
from twisted.application.service import IServiceMaker
from twisted.internet.protocol import Factory, Protocol
from twisted.plugin import IPlugin
from twisted.python.usage import Options
from zope.interface import implements
policy = '\n<cross-domain-policy>\n    <allow-access-from domain="*" to-ports="*" />\n</cross-domain-policy>\n'

class PolicyProtocol(Protocol):

    def connectionMade(self):
        self.transport.write(policy)
        self.transport.loseConnection()


class PolicyFactory(Factory):
    protocol = PolicyProtocol


class PolicyOptions(Options):
    pass


class PolicyServiceMaker(object):
    implements(IPlugin, IServiceMaker)
    tapname = 'flashpolicy'
    description = 'Permissive Flash policy server'
    options = PolicyOptions

    def makeService(self, options):
        """
        Set up a policy server.
        """
        return TCPServer(843, PolicyFactory())


servicemaker = PolicyServiceMaker()