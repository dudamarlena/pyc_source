# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/api/message/test/test_input.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.api.message.input}.
"""
from twisted.trial import unittest
from spamfighter.api.message.input import MessageInputCommand
from spamfighter.core.commands.partner import PartnerAuthInfo
from spamfighter.core.message import TransitMessage

class MessageInputCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.message.input.MessageInputCommand}.
    """

    def testRun(self):
        c = MessageInputCommand()
        c.params.partner = PartnerAuthInfo(None)
        c.params.message = TransitMessage(serialized={'text': 'Is this SPAM?'})
        return c.run().addCallback(lambda _: self.assertEqual('UNKNOWN', c.result.result))