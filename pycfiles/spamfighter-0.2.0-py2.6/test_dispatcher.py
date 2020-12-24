# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/commands/test/test_dispatcher.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.core.commands.dispatcher}.
"""
from twisted.trial import unittest
from spamfighter.core.commands import errors
from spamfighter.core.commands.command import Command
from spamfighter.core.commands.dispatcher import dispatchCommand, installCommand, deinstallCommand

class FakeCommand(Command):
    commandName = 'sf.test.fake'
    commandSignature = {}
    resultSignature = {}


class CommandDispatchTestCase(unittest.TestCase):
    """
    Тестируем диспетчеризацию комманд.
    """

    def testDispatchAbsent(self):
        self.assertRaises(errors.CommandUnknownException, dispatchCommand, 'sf.test.absent')

    def testDispatchOK(self):
        installCommand(FakeCommand)
        self.assert_(type(dispatchCommand('sf.test.fake')) is FakeCommand)
        deinstallCommand(FakeCommand)

    def testDoubleInstall(self):
        installCommand(FakeCommand)
        self.assertRaises(AssertionError, installCommand, FakeCommand)
        deinstallCommand(FakeCommand)