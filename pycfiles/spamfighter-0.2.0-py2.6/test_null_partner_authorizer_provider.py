# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/plugins/test/test_null_partner_authorizer_provider.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.plugins.null_partner_authorizer_provider}.
"""
import unittest
from zope.interface import verify as ziv
from twisted.plugin import IPlugin
from spamfighter.interfaces import IPartnerAuthorizer
from spamfighter.plugin import IPartnerAuthorizerProvider
from spamfighter.plugins.null_partner_authorizer_provider import nullPartnerAuthorizer, NullPartnerAuthorizerProvider

class NullPartnerAuthorizerProviderTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.plugins.null_partner_authorizer_provider.NullPartnerAuthorizerProvider}.
    """

    def testInterface(self):
        ziv.verifyClass(IPlugin, NullPartnerAuthorizerProvider)
        ziv.verifyClass(IPartnerAuthorizerProvider, NullPartnerAuthorizerProvider)

    def testGetAuthorizer(self):
        authorizer = nullPartnerAuthorizer.getPartnerAuthorizer()
        ziv.verifyObject(IPartnerAuthorizer, authorizer)