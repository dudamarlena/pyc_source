# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/model/test/test_command.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.core.model.command}.
"""
from twisted.trial import unittest
from zope.interface import implements
from spamfighter.core.commands import ICommand
from spamfighter.core.model.command import ModelBaseCommand
from spamfighter.core.model.bayes import BayesModel
from spamfighter.core.domain import getDefaultDomain

class FakeModelCommand(ModelBaseCommand):
    implements(ICommand)
    commandName = 'sf.test.model'
    commandSignature = {}
    resultSignature = {}

    def perform(self):
        return


class ModelBaseCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.core.model.command.ModelBaseCommand}.
    """

    def setUp(self):
        self.c = FakeModelCommand()
        self.model = BayesModel()
        getDefaultDomain().set('testMODEL', self.model)

    def tearDown(self):
        getDefaultDomain().delete('testMODEL')

    def testNoSuchModel(self):
        self.c.params.getUnserialized({'partner': None, 'model': 'noSuchModel', 'message': {}})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.AttributeKeyException'))

    def testNotAModel(self):
        self.c.params.getUnserialized({'partner': None, 'model': 'messageDomain', 'message': {}})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.NotAModelError'))

    def testGetModel(self):
        self.c.params.getUnserialized({'partner': None, 'model': 'testMODEL', 'message': {'text': ''}})
        return self.c.run().addCallback(lambda _: self.assert_(self.c.model is self.model))

    def testGetNoText(self):
        self.c.params.getUnserialized({'partner': None, 'model': 'testMODEL', 'message': {}})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.MessageAttributeKeyException'))

    def testGetText1(self):
        self.c.params.getUnserialized({'partner': None, 'model': 'testMODEL', 'message': {'text': 'Hoora!'}})
        return self.c.run().addCallback(lambda _: self.assertEqual('Hoora!', self.c.text))

    def testGetText2(self):
        self.c.params.getUnserialized({'partner': None, 'model': 'testMODEL', 'message': {'text': 'Hoora!'}, 'text_attribute': 'text1'})
        return self.c.run().addCallback(lambda _: self.assert_(False)).addErrback(lambda failure: failure.trap('spamfighter.core.commands.errors.MessageAttributeKeyException'))