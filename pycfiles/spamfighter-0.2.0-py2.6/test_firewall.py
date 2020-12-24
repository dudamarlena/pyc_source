# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/api/message/test/test_firewall.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.api.message.firewall}.
"""
from twisted.trial import unittest
from zope.interface import implements
from spamfighter.core.commands import ICommand
from spamfighter.api.message.firewall import FirewallCommand, FirewallRulesGetCommand, FirewallRulesSetCommand, FirewallRulesCheckCommand
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.firewall import MessageFirewall

class FakeFirewallCommand(FirewallCommand):
    implements(ICommand)
    commandName = 'sf.test.firewall'
    commandSignature = {}
    resultSignature = {}

    def perform(self):
        return


class FirewallCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.message.firewall.FirewallCommand}.
    """

    def setUp(self):
        self.c = FakeFirewallCommand()
        self.firewall = MessageFirewall()
        getDefaultDomain().set('testFIREWALL', self.firewall)

    def tearDown(self):
        getDefaultDomain().delete('testFIREWALL')

    def testNoSuchFirewall(self):
        self.c.params.getUnserialized({'partner': None, 'firewall': 'noSuchFirewall'})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.AttributeKeyException'))

    def testNotAFirewall(self):
        self.c.params.getUnserialized({'partner': None, 'firewall': 'messageDomain'})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.NotAFirewallError'))

    def testGetFirewall(self):
        self.c.params.getUnserialized({'partner': None, 'firewall': 'testFIREWALL'})
        return self.c.run().addCallback(lambda _: self.assert_(self.c.firewall is self.firewall))


class FirewallRulesGetCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.message.firewall.FirewallRulesGetCommand}.
    """

    def setUp(self):
        self.c = FirewallRulesGetCommand()
        self.firewall = MessageFirewall('stop as SPAMMER')
        getDefaultDomain().set('testFIREWALL', self.firewall)

    def tearDown(self):
        getDefaultDomain().delete('testFIREWALL')

    def testRun(self):
        self.c.params.getUnserialized({'partner': None, 'firewall': 'testFIREWALL'})
        return self.c.run().addCallback(lambda _: self.assertEquals('stop as SPAMMER', self.c.result.rules))


class FirewallRulesSetCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.message.firewall.FirewallRulesSetCommand}.
    """

    def setUp(self):
        self.c = FirewallRulesSetCommand()
        self.firewall = MessageFirewall()
        getDefaultDomain().set('testFIREWALL', self.firewall)

    def tearDown(self):
        getDefaultDomain().delete('testFIREWALL')

    def testRun(self):
        self.c.params.getUnserialized({'partner': None, 'firewall': 'testFIREWALL', 'rules': 'stop as TEST'})
        return self.c.run().addCallback(lambda _: self.assertEquals('stop as TEST', self.firewall.getRules()))

    def testRun(self):
        self.c.params.getUnserialized({'partner': None, 'firewall': 'testFIREWALL', 'rules': 'YYYY'})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.FirewallSyntaxError'))


class FirewallRulesCheckCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.message.firewall.FirewallRulesCheckCommand}.
    """

    def setUp(self):
        self.c = FirewallRulesCheckCommand()
        self.firewall = MessageFirewall('stop as SPAM')
        getDefaultDomain().set('testFIREWALL', self.firewall)

    def tearDown(self):
        getDefaultDomain().delete('testFIREWALL')

    def testRun(self):
        self.c.params.getUnserialized({'partner': None, 'firewall': 'testFIREWALL', 'rules': 'stop as TEST'})
        return self.c.run().addCallback(lambda _: self.assertEquals('stop as SPAM', self.firewall.getRules()))

    def testRun(self):
        self.c.params.getUnserialized({'partner': None, 'firewall': 'testFIREWALL', 'rules': 'YYYY'})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.FirewallSyntaxError'))