# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/partner.py
# Compiled at: 2009-01-30 08:10:10
"""
Базовые классы и методы работы с партнерами.
"""
from spamfighter.plugin import loadPlugin, IPartnerAuthorizerProvider
from spamfighter.utils import config

class PartnerAuthorizationFailedError(Exception):
    """
    Авторизация партнера была неуспешной.
    """
    pass


defaultPartnerAuthorizer = None

def getPartnerAuthorizer():
    u"""
    Получить текущий механизм авторизации партнеров.

    @return: механизм авторизации партнеров
    @rtype: L{spamfighter.interfaces.IPartnerAuthorizer}
    """
    global defaultPartnerAuthorizer
    if defaultPartnerAuthorizer is None:
        defaultPartnerAuthorizer = getPartnerAuthorizerProvider().getPartnerAuthorizer()
    return defaultPartnerAuthorizer


defaultPartnerAuthorizerProvider = None

def getPartnerAuthorizerProvider():
    u"""
    Получить провайдер авторизации партнеров.

    Загружаем как плагин, предсоставляющий интерфейс L{IPartnerAuthorizerProvider} с именем 
    из конфига: config.plugins.partner.default_provider

    @return: провайдер авторизации партнеров
    @rtype: L{IPartnerAuthorizerProvider}
    """
    global defaultPartnerAuthorizerProvider
    if defaultPartnerAuthorizerProvider is None:
        defaultPartnerAuthorizerProvider = loadPlugin(IPartnerAuthorizerProvider, config.plugins.partner.default_provider)
    return defaultPartnerAuthorizerProvider