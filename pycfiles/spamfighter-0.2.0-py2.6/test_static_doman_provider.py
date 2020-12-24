# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/plugins/test/test_static_doman_provider.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.plugins.static_domain_provider}.
"""
import unittest
from zope.interface import verify as ziv
from twisted.plugin import IPlugin
from spamfighter.interfaces import IDomain
from spamfighter.plugin import IDefaultDomainProvider
from spamfighter.plugins.static_domain_provider import emptyDomainProvider, StaticDefaultDomainProvider

class StaticDefaultDomainProviderTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.plugins.static_domain_provider.StaticDefaultDomainProvider}.
    """

    def testInterface(self):
        ziv.verifyClass(IPlugin, StaticDefaultDomainProvider)
        ziv.verifyClass(IDefaultDomainProvider, StaticDefaultDomainProvider)

    def testEmptyDomain(self):
        domain = emptyDomainProvider.getDefaultDomain()
        ziv.verifyObject(IDomain, domain)