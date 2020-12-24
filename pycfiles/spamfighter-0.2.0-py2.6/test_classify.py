# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/api/model/test/test_classify.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.api.model.classify}.
"""
from twisted.trial import unittest
from spamfighter.api.model.classify import ModelClassifyCommand
from spamfighter.core.commands.partner import PartnerAuthInfo
from spamfighter.core.message import TransitMessage
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.model.bayes import BayesModel

class ModelClassifyCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.model.classify.ModelClassifyCommand}.
    """

    def setUp(self):
        model = BayesModel()
        model.train('мама мыла раму', True)
        model.train('папа пошел гулять', False)
        getDefaultDomain().set('testModel', model)

    def tearDown(self):
        getDefaultDomain().delete('testModel')

    def testRun1(self):
        c = ModelClassifyCommand()
        c.params.partner = PartnerAuthInfo(None)
        c.params.message = TransitMessage(serialized={'text': 'мама'})
        c.params.model = 'testModel'
        return c.run().addCallback(lambda _: self.assert_(c.result.marker == 'good'))

    def testRun2(self):
        c = ModelClassifyCommand()
        c.params.partner = PartnerAuthInfo(None)
        c.params.message = TransitMessage(serialized={'text': 'папа'})
        c.params.model = 'testModel'
        return c.run().addCallback(lambda _: self.assert_(c.result.marker == 'bad'))