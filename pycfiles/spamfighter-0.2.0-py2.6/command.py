# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/model/command.py
# Compiled at: 2009-01-30 08:10:10
"""
Базовый класс команд работы с моделью.
"""
import types
from zope.interface import providedBy
from twisted.internet import defer
from spamfighter.interfaces import IModel
from spamfighter.core.commands import DomainedCommand, errors
from spamfighter.core.domain import DomainKeyError
from spamfighter.core.message import ITransitMessage, AttributeNotFoundError

class ModelBaseCommand(DomainedCommand):
    """
    Базовый класс команд, упраявляющих моделью.

    @ivar model: модель, которой мы управляем
    @type model: L{IModel}
    @ivar message: сообщение, на котором мы тренируемся
    @type message: L{IMessage}
    @ivar text: извлеченный текст сообщения
    @type text: C{unicode}
    """
    commandSignature = {'model': {'type': types.StringType, 'required': True}, 'message': {'type': ITransitMessage, 'required': True}, 'text_attribute': {'type': types.StringType, 'required': False}}

    def init(self):
        u"""
        Дополнительный метод, может переопределяться в потомках для выполнения процедуры
        дополнительной предварительной инициализации.

        Находим домен по пути из корневого.
        """

        def doIt(_):
            try:
                self.model = self.domain.get(self.params.model)
            except DomainKeyError:
                raise errors.AttributeKeyException, self.params.model

            if not IModel.providedBy(self.model):
                raise errors.NotAModelError, self.params.model
            self.message = self.params.message.getMessage(self.domain)
            if self.params.text_attribute is None:
                self.params.text_attribute = 'text'
            try:
                self.text = self.message[self.params.text_attribute].value()
            except AttributeNotFoundError:
                raise errors.MessageAttributeKeyException, self.params.text_attribute

            return

        return defer.maybeDeferred(super(ModelBaseCommand, self).init).addCallback(doIt)