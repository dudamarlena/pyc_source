# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/commands/errors.py
# Compiled at: 2009-01-30 08:10:10
"""
Базовые классы обработки ошибок при выполнении команд.
"""
from string import Template
import types

class BaseCommandException(Exception):
    """
    Базовое исключение при обработке команды
    """

    def __init__(self, **args):
        self.code = self.getCode()
        self.message = Template(self.getMessage().decode('utf-8')).safe_substitute(args)

    def getCode(self):
        return self.code

    def getMessage(self):
        return self.message

    def __str__(self):
        return self.getMessage().encode('utf-8')


class InternalCommandException(BaseCommandException):
    """
    Сообщение о внутренней ошибке сервера.
    Не должно происходить при нормальной работе.
    """
    pass


class FatalCommandException(BaseCommandException):
    """
    Фатальная ошибка, приводящая к закрытию текущего соединения.
    После неё выполнение продолжено быть не может.
    """
    pass


class UnexpectedException(InternalCommandException):
    """
    Исключение об неизвестной ситуации при обработке команды
    """
    code = 99000
    message = 'Неизвестная ошибка при обработке команды'

    def __init__(self):
        BaseCommandException.__init__(self)


class CommandResultMissingException(InternalCommandException):
    """
    Исключение об отсутствии результата команды
    """
    code = 99002
    message = 'Не найден обязательный параметр $param результата'

    def __init__(self, param):
        BaseCommandException.__init__(self, param=param)


class CommandParamsMissingException(BaseCommandException):
    """
    Исключение об отсутствии параметров команды
    """
    code = 1001
    message = 'Не найден обязательный параметр $param команды'

    def __init__(self, param):
        BaseCommandException.__init__(self, param=param)


class CommandUnknownException(BaseCommandException):
    """
    Исключение о неизвестной команде. 
    """
    code = 1002
    message = 'Команда $command не поддерживается'

    def __init__(self, command):
        BaseCommandException.__init__(self, command=command)


class UnknownParameterException(BaseCommandException):
    """
    Исключение о передаче неизвестного параметра для команды. 
    """
    code = 1004
    message = 'Параметр $param не известен в контексте данной команды'

    def __init__(self, param):
        BaseCommandException.__init__(self, param=param)


class TypeParameterException(BaseCommandException):
    """
    Исключение о передаче параметра неверного типа. 
    """
    code = 1005
    message = 'Параметр $param неподдерживаемого типа'

    def __init__(self, param):
        BaseCommandException.__init__(self, param=param)


class AuthorizationFailedException(BaseCommandException):
    """
    Авторизация через партнера не удалась.
    """
    code = 2001
    message = 'Авторизация неуспешная. Проверьте параметры партнера'


class DomainPathNotFoundException(BaseCommandException):
    """
    Указанный путь к домену не валиден.
    """
    code = 2002
    message = 'Указанный путь $path к домену не существует'

    def __init__(self, path):
        BaseCommandException.__init__(self, path=path)


class AttributeKeyException(BaseCommandException):
    """
    Атрибут не найден в домене.
    """
    code = 2003
    message = 'В описании текущего домена отсутствует атрибут $param'

    def __init__(self, param):
        BaseCommandException.__init__(self, param=param)


class SkipToFallthroughError(BaseCommandException):
    """
    В firewall не нашлось метки для skip to...
    """
    code = 2004
    message = 'Для правила skip to $label не была обнаружена соответствующая метка $label'

    def __init__(self, label):
        BaseCommandException.__init__(self, label=label)


class NotAModelError(BaseCommandException):
    """
    Указанный объект не является моделью.
    """
    code = 2005
    message = 'Объект домена $param не является моделью'

    def __init__(self, param):
        BaseCommandException.__init__(self, param=param)


class MessageAttributeKeyException(BaseCommandException):
    """
    Атрибут не найден в сообщении.
    """
    code = 2006
    message = 'В сообщении отсутствует атрибут $param'

    def __init__(self, param):
        BaseCommandException.__init__(self, param=param)


class NotAFirewallError(BaseCommandException):
    """
    Указанный объект не является firewallом.
    """
    code = 2007
    message = 'Объект домена $param не является firewallом'

    def __init__(self, param):
        BaseCommandException.__init__(self, param=param)


class FirewallSyntaxError(BaseCommandException):
    """
    Ошибка синтаксиса правил firewall.
    """
    code = 2008
    message = 'Ошибка синтаксиса правил firewall: $message'

    def __init__(self, message):
        BaseCommandException.__init__(self, message=message)


class NotAMessageLogError(BaseCommandException):
    """
    Указанный объект не является логом сообщений.
    """
    code = 2009
    message = 'Объект домена $param не является логом сообщений'

    def __init__(self, param):
        BaseCommandException.__init__(self, param=param)