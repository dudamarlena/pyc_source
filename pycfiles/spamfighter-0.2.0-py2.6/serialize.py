# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/message/serialize.py
# Compiled at: 2009-01-30 08:10:10
"""
Сериализация сообщений, взаимодействие с командами.
"""
from zope.interface import implements
from twisted.internet import defer
from spamfighter.interfaces import IMessage
from spamfighter.core.commands.serialize import ISerializable, register_serializer
from spamfighter.core.commands import errors
from spamfighter.core.message.message import Message

class ITransitMessage(ISerializable):
    """
    Вариант сообщения, которое передается в сериализованном представлении
    через параметры команд.
    """

    def getMessage(domain):
        u"""
        Окончательно десериализовать сообщение относительно домена.

        @param domain: домен, относительно которого десериализуется сообщение
        @type domain: L{spamfighter.interfaces.IDomain}
        """
        pass


class TransitMessage(object):
    """
    Вариант сообщения, которое передается в сериализованном представлении
    через параметры команд.

    @ivar serialized: сериализованное представление сообщения
    @type serialized: C{dict}
    """
    implements(ITransitMessage)
    register_serializer(ITransitMessage)

    def __init__(self, message=None, serialized=None):
        u"""
        Конструктор.

        Может быть передано либо сериализованное представление сообщения (C{serialized}), либо
        исходное сообщение (C{message}).

        @param message: исходное сообщение
        @type message: L{IMessage}
        @param serialized: сериализованное представление сообщения
        @type serialized: C{dict}
        """
        if serialized is not None:
            assert message is None
            self.serialized = serialized
        else:
            assert serialized is None
            assert IMessage.providedBy(message)
            self.serialized = {}
            for attribute in message:
                self.serialized[attribute.domain().name()] = attribute.serialize()

            return

    def serialize(self):
        u"""
        Сериализовать сообщение.
        """
        return defer.succeed(self.serialized)

    @classmethod
    def unserialize(cls, serialized):
        u"""
        Десериализовать сообщение.

        @param serialized: сериализованное представление сообщения
        @type serialized: C{dict}
        """
        return TransitMessage(serialized=serialized)

    def getMessage(self, domain):
        u"""
        Окончательно десериализовать сообщение относительно домена.

        @param domain: домен, относительно которого десериализуется сообщение
        @type domain: L{spamfighter.interfaces.IDomain}
        @return: десериализованное сообщение
        @rtype: L{IMessage}
        """
        messageDomain = domain.get('messageDomain')
        try:
            return Message([ messageDomain[name].deserialize(value) for (name, value) in self.serialized.iteritems() ])
        except KeyError, name:
            raise errors.AttributeKeyException(name)

    def __repr__(self):
        return 'TransitMessage(serialized=%r)' % self.serialized

    def __eq__(self, other):
        if not isinstance(other, TransitMessage):
            return False
        return self.serialized == other.serialized