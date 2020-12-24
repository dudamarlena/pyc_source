# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/rules/test/test_analyze.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.rules.analyze}.
"""
from twisted.trial import unittest
from spamfighter.rules.analyze import messageFloodCheck
from spamfighter.core.message import TransitMessage
from spamfighter.core.domain import getDefaultDomain

class AnalyzeRulesTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.rules.text}.
    """

    def setUp(self):
        self.message5 = TransitMessage(serialized={'text': '!!!!!!!!!!!!!!!!!!!!!!', 'from': 16}).getMessage(getDefaultDomain())
        self.message6 = TransitMessage(serialized={'text': 'покажи сиськи! покажи сиськи! покажи сиськи! покажи сиськи! покажи сиськи! покажи сиськи! покажи сиськи! покажи сиськи!', 'from': 16}).getMessage(getDefaultDomain())

    def tearDown(self):
        pass

    def testAnalyzeMessage(self):
        self.assertFalse(messageFloodCheck(domain=getDefaultDomain(), message=self.message5))
        self.assertTrue(messageFloodCheck(domain=getDefaultDomain(), message=self.message5, minLength=30))
        self.assertFalse(messageFloodCheck(domain=getDefaultDomain(), message=self.message6))