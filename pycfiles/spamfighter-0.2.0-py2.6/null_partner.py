# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/null_partner.py
# Compiled at: 2009-01-30 08:10:10
"""
Модуль авторизации партнеров без логинов/паролей (на доверии).
"""
from zope.interface import implements
from twisted.internet import defer
from spamfighter.interfaces import IPartner, IPartnerAuthorizer
from spamfighter.core.partner import PartnerAuthorizationFailedError
from spamfighter.core.domain import getDefaultDomain, BaseDomain
from spamfighter.plugin import loadPlugin, IDefaultDomainProvider
from spamfighter.utils import config

class NullPartner(object):
    """
    Партнер, авторизованный без логина/пароля (на доверии).

    @ivar domain: корневой домен партнера
    @type domain: L{BaseDomain}
    """
    implements(IPartner)

    def __init__(self):
        u"""
        Конструктор.
        """
        domainProvider = loadPlugin(IDefaultDomainProvider, config.plugins.domain.null_partner_domain_provider)
        self.domain = domainProvider.getDefaultDomain()

    def rootDomain(self):
        u"""
        Получить корневой домен партнера.

        @return: Deferred, корневой домен (L{IDomain})
        @rtype: C{twisted.internet.defer.Deferred} 
        """
        return defer.succeed(self.domain)


class NullPartnerAuthorizer(object):
    """
    Провайдер авторизации партнеров без логина/пароля (на доверии).

    В этой ситуации доступ к СпамоБорцу ограничен с помощью других средств
    (HTTP-proxy, firewall).

    @ivar partner: единственный партнер, который обеспечивает весь доступ
    @type partner: L{NullPartner}
    """
    implements(IPartnerAuthorizer)

    def __init__(self):
        u"""
        Конструктор.
        """
        self.partner = NullPartner()

    def authorize(self, partner_info):
        u"""
        Выполнить авторизацию партнера.

        @param partner_info: информация о партнере
        @return: Deferred, партнер (L{IPartner})
        @rtype: C{twisted.internet.defer.Deferred} 
        """
        if partner_info is not None:
            return defer.fail(PartnerAuthorizationFailedError())
        else:
            return defer.succeed(self.partner)