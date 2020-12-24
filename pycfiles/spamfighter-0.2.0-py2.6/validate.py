# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/rules/validate.py
# Compiled at: 2009-01-30 08:10:10
"""
Модуль содержащий правила проверки сообщений
"""
import re
from spamfighter.core.rules import factory
from spamfighter.core.message.attribute import AttributeNotFoundError

class regexpCheck(object):
    """
    Правило проверки текст сообщение на соответствие регулярному выражению.

    @ivar compiledRe: скомпилированное регулярное выражение
    @type compiledRe: C{re}
    """

    def __init__(self, regexp):
        u"""
        Конструктор.

        @param regexp: регулярное выражение для анализа
        @type regexp: C{unicode}
        """
        self.compiledRe = re.compile(regexp, re.U)

    def analyze(self, domain, message, attribute='text'):
        u"""
        Функция анализа сообщения на соответствие регулярному выражению

        @param domain: домен, относительно которого идёт анализ
        @type domain: L{IDomain}
        @param message: сообщение
        @type message: L{spamfighter.interfaces.IMessage}
        @param attribute: имя атрибута сообщения, содержащего текст
        @type attribute: C{str}
        """
        return self.compiledRe.match(message.get(attribute).value()) is not None


def lengthCheck(domain, message, minLength=None, maxLength=None, attribute='text'):
    u"""
    Правило проверки текста сообщение на минимальную и максимальную длину.

    @param domain: домен, относительно которого идёт анализ
    @type domain: L{IDomain}
    @param message: сообщение
    @type message: L{spamfighter.interfaces.IMessage}
    @param attribute: имя атрибута сообщения, содержащего текст
    @type attribute: C{str}
    @param minLength: минимальная длина сообщения
    @type minLength: C{int}
    @param minLength: максимальная длина сообщения
    @type minLength: C{int}
    """
    if minLength is not None and len(message.get(attribute).value()) < minLength:
        return False
    else:
        if maxLength is not None and len(message.get(attribute).value()) > maxLength:
            return False
        return True


def attributeCheck(domain, message, attribute, value):
    u"""
    Правило проверки соответствия значения атрибута указанному значению.

    @param domain: домен, относительно которого идёт анализ
    @type domain: L{IDomain}
    @param message: сообщение
    @type message: L{spamfighter.interfaces.IMessage}
    @param attribute: имя атрибута сообщения для проверки на соответствие
    @type attribute: C{str}
    @param value: значение для проверки на соответствие
    @type value: C{object}
    """
    return message.get(attribute).value() == value


def hasAttribute(domain, message, attribute):
    u"""
    Правило проверки наличия аттрибута у сообщения

    @param domain: домен, относительно которого идёт анализ
    @type domain: L{IDomain}
    @param message: сообщение
    @type message: L{spamfighter.interfaces.IMessage}
    @param attribute: имя атрибута сообщения для проверки на наличие
    @type attribute: C{str}
    """
    try:
        message.get(attribute)
        return True
    except AttributeNotFoundError:
        return False


factory.registerRule(regexpCheck)
factory.registerRule(lengthCheck)
factory.registerRule(hasAttribute)
factory.registerRule(attributeCheck)