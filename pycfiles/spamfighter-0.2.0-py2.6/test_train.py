# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/api/model/test/test_train.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.api.model.train}.
"""
from twisted.trial import unittest
from spamfighter.api.model.train import ModelTrainCommand
from spamfighter.core.commands.partner import PartnerAuthInfo
from spamfighter.core.message import TransitMessage
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.model.bayes import BayesModel

class ModelTrainCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.model.train.ModelTrainCommand}.
    """

    def setUp(self):
        getDefaultDomain().set('testModel', BayesModel())

    def tearDown(self):
        getDefaultDomain().delete('testModel')

    def testRun(self):
        c = ModelTrainCommand()
        c.params.partner = PartnerAuthInfo(None)
        c.params.message = TransitMessage(serialized={'text': 'Is this SPAM?'})
        c.params.marker = 'bad'
        c.params.model = 'testModel'
        return c.run()

    def testBadMarker(self):
        c = ModelTrainCommand()
        c.params.partner = PartnerAuthInfo(None)
        c.params.message = TransitMessage(serialized={'text': 'Is this SPAM?'})
        c.params.marker = '?'
        c.params.model = 'testModel'
        return c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.TypeParameterException'))