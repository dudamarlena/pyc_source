# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/commands/test/test_partner.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.core.commands.partner}.
"""
from twisted.trial import unittest
from zope.interface import implements
from spamfighter.interfaces import IPartner, IDomain
from spamfighter.core.commands import command
from spamfighter.core.commands.partner import PartneredCommand, DomainedCommand

class FakePartneredCommand(PartneredCommand):
    implements(command.ICommand)
    commandName = 'sf.test.partnered'
    commandSignature = {}
    resultSignature = {}

    def perform(self):
        return


class FakeDomainedCommand(DomainedCommand):
    implements(command.ICommand)
    commandName = 'sf.test.domained'
    commandSignature = {}
    resultSignature = {}

    def perform(self):
        return


class PartneredCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.commands.partner.PartneredCommand}.
    """

    def setUp(self):
        self.c = FakePartneredCommand()

    def testAuthOK(self):
        self.c.params.getUnserialized({'partner': None})
        return self.c.run().addCallback(lambda _: self.assert_(IPartner.providedBy(self.c.partner)))

    def testAuthFail(self):
        self.c.params.getUnserialized({'partner': 111})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.AuthorizationFailedException'))


class DomainedCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.commands.partner.DomainedCommand}.
    """

    def setUp(self):
        self.c = FakeDomainedCommand()

    def testDomainOk(self):
        self.c.params.getUnserialized({'partner': None})
        return self.c.run().addCallback(lambda _: self.assert_(IPartner.providedBy(self.c.partner))).addCallback(lambda _: self.assert_(IDomain.providedBy(self.c.domain)))

    def testDomainFail(self):
        self.c.params.getUnserialized({'partner': None, 'domain': 'no/such/domain'})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.DomainPathNotFoundException'))