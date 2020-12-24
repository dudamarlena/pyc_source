# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/rules/test/test_model.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.rules.model}.
"""
from twisted.trial import unittest
from twisted.internet import defer
from spamfighter.rules.model import modelClassify, modelTrain
from spamfighter.core.message import TransitMessage
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.model.bayes import BayesModel

class ModelRuleTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.rules.model}.
    """

    def setUp(self):
        model = BayesModel()
        model.train('мама мыла раму', True)
        model.train('папа пошел гулять', False)
        getDefaultDomain().set('testModel', model)
        self.message1 = TransitMessage(serialized={'text': 'мама'}).getMessage(getDefaultDomain())
        self.message2 = TransitMessage(serialized={'text': 'папа'}).getMessage(getDefaultDomain())

    def tearDown(self):
        getDefaultDomain().delete('testModel')

    def testNoModel(self):
        return defer.maybeDeferred(modelClassify(model='__noSUCHMODEL__').analyze, domain=getDefaultDomain(), message=self.message1).addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.AttributeKeyException'))

    def testNotAModel(self):
        return defer.maybeDeferred(modelClassify(model='messageDomain').analyze, domain=getDefaultDomain(), message=self.message1).addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.NotAModelError'))

    def testNoAttribute(self):
        return defer.maybeDeferred(modelClassify(model='testModel').analyze, domain=getDefaultDomain(), message=self.message1, attribute='noSuch').addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.MessageAttributeKeyException'))

    def testClassify1(self):
        return modelClassify(model='testModel').analyze(domain=getDefaultDomain(), message=self.message1).addCallback(self.assertTrue)

    def testClassify2(self):
        return modelClassify(model='testModel').analyze(domain=getDefaultDomain(), message=self.message2).addCallback(self.assertFalse)

    def testTrain(self):
        return modelTrain(model='testModel').analyze(domain=getDefaultDomain(), message=self.message2, marker='good').addCallback(self.assertTrue)