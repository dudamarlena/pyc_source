# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/plugin.py
# Compiled at: 2009-01-30 08:10:10
"""
Подсистема плагинов СпамоБорца и интерфейсы плагинов.
"""
from twisted.plugin import getPlugins
from zope.interface import Interface

class INamedPlugin(Interface):
    """
    Базовый интерфейс плагинов: плагин, который имеет имя.
    """

    def name():
        u"""
        Получить имя плагина.

        @return: имя плагина
        @rtype: C{str}
        """
        pass


class IDefaultDomainProvider(INamedPlugin):
    """
    Интерфейс плагина, возвращающего ссылку на провайдер домена по умолчанию. 
    """

    def getDefaultDomain():
        u"""
        Получить домен по умолчанию в системе.

        @return: домен по умолчанию.
        @rtype: L{spamfighter.interfaces.IDomain}
        """
        pass


class IPartnerAuthorizerProvider(INamedPlugin):
    """
    Интерфейс плагина, возвращающего ссылку на механизм авторизации партнеров. 
    """

    def getPartnerAuthorizer():
        u"""
        Получить механизм авторизации партнеров.

        @return: домен по умолчанию.
        @rtype: L{spamfighter.interfaces.IPartnerAuthorizer}
        """
        pass


class PluginNotFoundError(Exception):
    """
    Не найден плагин с указанным именем.
    """
    pass


class PluginAmbiguityError(Exception):
    """
    Найдено более одного плагина с указанным именем.
    """
    pass


def loadPlugin(interface, name, package=None):
    u"""
    Загрузить указанный плагин СпамоБорца. Возвращает
    экземлпяр объекта плагина.

    @param interface: интерфейс, который должен реализовывать плагин
    @param name: имя плагина (см. L{INamedPlugin})
    @type name: C{str}
    """
    if package == None:
        import spamfighter.plugins
        package = spamfighter.plugins
    plugins = filter(lambda plugin: plugin.name() == name, getPlugins(interface, package))
    if len(plugins) == 0:
        raise PluginNotFoundError, name
    if len(plugins) > 1:
        raise PluginAmbiguityError, name
    return plugins[0]