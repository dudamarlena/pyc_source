# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/message/test/test_serialize.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.core.message.serialize}.
"""
from zope.interface import verify as ziv
from twisted.trial import unittest
from spamfighter.core.message.serialize import ITransitMessage, TransitMessage
from spamfighter.core.message.attribute import Attribute, TextAttributeDomain, IntAttributeDomain
from spamfighter.core.message.message import Message, MessageDomain
from spamfighter.core.domain import BaseDomain
from spamfighter.core.commands import errors

class TransitMessageTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.message.TransitMessage}.
    """

    def setUp(self):
        self.ta1 = TextAttributeDomain('string1')
        self.ta2 = TextAttributeDomain('string2')
        self.ta3 = TextAttributeDomain('string3')
        self.ta4 = IntAttributeDomain('int1')
        self.messageDomain = MessageDomain(self.ta1, self.ta2, self.ta3, self.ta4)
        self.domain = BaseDomain(dict={'messageDomain': self.messageDomain}, key='d')

    def testInterface(self):
        ziv.verifyClass(ITransitMessage, TransitMessage)

    def testSerialize1(self):
        return TransitMessage(message=Message([])).serialize().addCallback(lambda result: self.assertEquals({}, result))

    def testSerialize2(self):
        return TransitMessage(message=Message([Attribute(self.ta1, 'Тестовый текст'), Attribute(self.ta2, 'DDD')])).serialize().addCallback(lambda result: self.assertEquals({'string1': 'Тестовый текст', 'string2': 'DDD'}, result))

    def testSerialize3(self):
        return TransitMessage(message=Message([Attribute(self.ta1, 'Тестовый текст'), Attribute(self.ta4, 1228)])).serialize().addCallback(lambda result: self.assertEquals({'string1': 'Тестовый текст', 'int1': 1228}, result))

    def testSerialize4(self):
        self.assertEquals(Message([Attribute(self.ta1, 'Тестовый текст'), Attribute(self.ta3, 'Lalala!')]), TransitMessage(serialized={'string1': '   Тестовый текст   ', 'string3': 'Lalala! '}).getMessage(self.domain))

    def testDeserialize(self):
        self.assertEquals(Message([Attribute(self.ta1, 'Тестовый текст'), Attribute(self.ta3, 'Lalala!')]), TransitMessage(serialized={'string1': 'Тестовый текст', 'string3': 'Lalala!'}).getMessage(self.domain))
        self.assertEquals(Message([Attribute(self.ta1, 'Тестовый текст'), Attribute(self.ta4, 1234)]), TransitMessage(serialized={'string1': 'Тестовый текст', 'int1': 1234}).getMessage(self.domain))
        self.assertEquals(Message([]), TransitMessage(serialized={}).getMessage(self.domain))
        self.assertRaises(errors.AttributeKeyException, TransitMessage(serialized={'no-such-property': 'aaa'}).getMessage, self.domain)