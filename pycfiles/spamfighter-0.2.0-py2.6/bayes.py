# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/model/bayes.py
# Compiled at: 2009-01-30 08:10:10
"""
Модель анализа сообщений по Байесу.
"""
from zope.interface import implements
from twisted.internet import defer
from spamfighter.interfaces import IModel
from spamfighter.core.model.thomas import Bayes

class BayesModel(object):
    """
    Модель анализа сообщений по Байесу.

    @ivar bayes: анализатор по Байесу
    @type bayes: L{Bayes}
    """
    implements(IModel)

    def __init__(self):
        u"""
        Конструктор.
        """
        self.bayes = Bayes()

    def train(self, text, good):
        u"""
        Обучить модель на указанном тексте.

        @param text: текст, на котором обучаемся
        @type text: C{unicode}
        @param good: хороший это текст или плохой с точки зрения классификации?
        @type good: C{bool}
        @return: результат операции
        @rtype: C{Deferred}
        """
        if good:
            pool = 'good'
        else:
            pool = 'bad'
        self.bayes.train(pool, text)
        return defer.succeed(True)

    def classify(self, text):
        u"""
        Классифицировать текст согласно модели.

        Результат классификации - текст "хороший" или "плохой" (относительно модели).

        @param text: текст, который классифируем
        @type text: C{unicode}
        @return: результат операции, C{bool}, хороший ли текст?
        @rtype: C{Deferred}
        """
        result = self.bayes.guess(text)
        if len(result) == 0:
            return defer.succeed(True)
        if 'bad' == result[0][0]:
            return defer.succeed(False)
        return defer.succeed(True)