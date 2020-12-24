# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/rules/log.py
# Compiled at: 2009-01-30 08:10:10
"""
Правила, управляющие логом сообщений.
"""
from spamfighter.core.rules import factory
from spamfighter.core.domain import DomainKeyError
from spamfighter.core.commands import errors
from spamfighter.interfaces import IMessageLog

def messageLogPut(domain, message, log='messageLog', tag=None):
    u"""
    Поместить сообщение в лог сообщений.

    Дополнительно можно при помещении в лог указать дополнительный тэг, который будет сохранен в логе
    вместе с сообщением.

    @param domain: домен, относительно которого идёт анализ
    @type domain: L{IDomain}
    @param message: сообщение
    @type message: L{spamfighter.interfaces.IMessage}
    @param log: имя свойства домена, содержащего лог сообщений
    @type log: C{str}
    @param tag: дополнительный тэг, записываемый в лог
    @type tag: C{str}
    """
    try:
        messageLog = domain.get(log)
    except DomainKeyError:
        raise errors.AttributeKeyException, log

    if not IMessageLog.providedBy(messageLog):
        raise errors.NotAMessageLogError, log
    if tag is None:
        tags = []
    else:
        tags = [
         tag]
    return messageLog.put(message=message, tags=tags).addCallback(lambda _: True)


factory.registerRule(messageLogPut)