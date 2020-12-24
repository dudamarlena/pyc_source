# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/plugins/null_partner_authorizer_provider.py
# Compiled at: 2009-01-30 08:10:10
"""
Плагин, реализующий авторизацию партнеров без логинов/паролей (доверительный вариант).
"""
from zope.interface import implements
from twisted.plugin import IPlugin
from spamfighter.plugin import IPartnerAuthorizerProvider
from spamfighter.core.null_partner import NullPartnerAuthorizer

class NullPartnerAuthorizerProvider(object):
    """
    Провайдер авторизации партнеров без логинов/паролей.
    """
    implements(IPlugin, IPartnerAuthorizerProvider)

    def __init__(self):
        u"""
        Конструктор.
        """
        pass

    def name(self):
        u"""
        Получить имя плагина.

        @return: имя плагина
        @rtype: C{str}
        """
        return 'NullPartnerAuthorizerProvider'

    def getPartnerAuthorizer(self):
        u"""
        Получить механизм авторизации партнеров.

        @return: домен по умолчанию.
        @rtype: L{spamfighter.interfaces.IPartnerAuthorizer}
        """
        return NullPartnerAuthorizer()


nullPartnerAuthorizer = NullPartnerAuthorizerProvider()