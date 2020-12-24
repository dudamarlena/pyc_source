# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/model/test/test_bayes.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.core.model.bayes}.
"""
from zope.interface import verify as ziv
from twisted.trial import unittest
from spamfighter.interfaces import IModel
from spamfighter.core.model.bayes import BayesModel
from spamfighter.core.model.test import Texts

class BayesModelTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.model.dm.BayesModel}.
    """

    def testInterface(self):
        ziv.verifyClass(IModel, BayesModel)

    def testTrainClassifySimple(self):
        model = BayesModel()
        model.train('мама мыла раму', True)
        model.train('папа пошел гулять', False)
        return model.classify('папа').addCallback(lambda result: self.assert_(not result)).addCallback(lambda _: model.classify('мама')).addCallback(lambda result: self.assert_(result))

    def testTrainClassify(self):
        model = BayesModel()
        model.train(Texts.pushkin2, True)
        model.train(Texts.udaff, False)
        return model.classify(Texts.udaff2).addCallback(lambda result: self.assert_(not result)).addCallback(lambda _: model.classify(Texts.pushkin)).addCallback(lambda result: self.assert_(result))