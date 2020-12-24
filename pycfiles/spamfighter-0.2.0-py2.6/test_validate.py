# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/rules/test/test_validate.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.rules.validate}.
"""
from twisted.trial import unittest
from spamfighter.rules.validate import regexpCheck, lengthCheck, attributeCheck, hasAttribute
from spamfighter.core.message import TransitMessage
from spamfighter.core.domain import getDefaultDomain

class ValidateRulesTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.rules.validate}.
    """

    def setUp(self):
        self.message1 = TransitMessage(serialized={'text': 'тестовое сообщение для анализа регуляркой'}).getMessage(getDefaultDomain())
        self.message2 = TransitMessage(serialized={'text': 'плохое тестовое сообщение для анализа регулиркой'}).getMessage(getDefaultDomain())
        self.message3 = TransitMessage(serialized={'text': 'среднее тестовое сообщение', 'from': 1212}).getMessage(getDefaultDomain())

    def tearDown(self):
        pass

    def testCheckRegexp1(self):
        self.assertTrue(regexpCheck(regexp='^тестовое ').analyze(domain=getDefaultDomain(), message=self.message1))

    def testCheckRegexp2(self):
        self.assertFalse(regexpCheck(regexp='^тестовое').analyze(domain=getDefaultDomain(), message=self.message2))

    def testCheckLength(self):
        self.assertFalse(lengthCheck(domain=getDefaultDomain(), message=self.message1, minLength=64))
        self.assertTrue(lengthCheck(domain=getDefaultDomain(), message=self.message1, minLength=10))

    def testCheckLength(self):
        self.assertTrue(lengthCheck(domain=getDefaultDomain(), message=self.message1))
        self.assertFalse(lengthCheck(domain=getDefaultDomain(), message=self.message1, minLength=64))
        self.assertTrue(lengthCheck(domain=getDefaultDomain(), message=self.message1, minLength=10))
        self.assertTrue(lengthCheck(domain=getDefaultDomain(), message=self.message1, maxLength=64))
        self.assertFalse(lengthCheck(domain=getDefaultDomain(), message=self.message1, maxLength=10))

    def testCheckAttribute(self):
        self.assertTrue(attributeCheck(domain=getDefaultDomain(), message=self.message3, attribute='from', value=1212))
        self.assertFalse(attributeCheck(domain=getDefaultDomain(), message=self.message3, attribute='from', value=1412))

    def testHasAttribute(self):
        self.assertFalse(hasAttribute(domain=getDefaultDomain(), message=self.message1, attribute='from'))
        self.assertTrue(hasAttribute(domain=getDefaultDomain(), message=self.message3, attribute='from'))