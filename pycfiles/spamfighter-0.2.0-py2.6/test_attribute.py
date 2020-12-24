# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/message/test/test_attribute.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.core.message.attribute}.
"""
from zope.interface import verify as ziv
from twisted.trial import unittest
from spamfighter.interfaces import IAttribute, IAttributeDomain
from spamfighter.core.message.attribute import Attribute, AttributeDomain, TextAttributeDomain, IntAttributeDomain

class AttributeDomainTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.message.attribute.AttributeDomain}.
    """

    def testInterface(self):
        ziv.verifyClass(IAttributeDomain, AttributeDomain)

    def testName(self):
        self.assertEquals('John', AttributeDomain('John').name())


class TextAttributeDomainTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.message.attribute.TextAttributeDomain}.
    """

    def testSerialize(self):
        ta = TextAttributeDomain('John')
        a = Attribute('John', 'Ураа!')
        self.assertEquals('Ураа!', ta.serialize(a))
        a = Attribute('John', 'Ураа!')
        self.assertEquals('Ураа!', ta.serialize(a))

    def testDeserialize(self):
        ta = TextAttributeDomain('John')
        self.assertEquals('Ураа!', ta.deserialize('Ураа!').value())
        self.assert_(ta is ta.deserialize('Ураа!').domain())
        self.assertEquals('Ураа!', ta.deserialize('Ураа!').value())

    def testDeserializeStrip(self):
        ta = TextAttributeDomain('John')
        self.assertEquals('Ураа!', ta.deserialize(' Ураа! ').value())


class IntAttributeDomainTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.message.attribute.IntAttributeDomain}.
    """

    def testSerialize(self):
        ta = IntAttributeDomain('John')
        a = Attribute('John', 1586)
        self.assertEquals(1586, ta.serialize(a))

    def estDeserialize(self):
        ta = IntAttributeDomain('John')
        self.assertEquals(1586, ta.deserialize(1586).value())
        self.assert_(ta is ta.deserialize(1586).domain())


class AttributeTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.message.attribute.Attribute}.
    """

    def setUp(self):
        self.attribute = Attribute(TextAttributeDomain('John'), 'abcd')

    def testInterface(self):
        ziv.verifyClass(IAttribute, Attribute)

    def testDomain(self):
        self.assertEquals(AttributeDomain('John'), self.attribute.domain())

    def testSerialize(self):
        self.assertEquals('abcd', self.attribute.serialize())