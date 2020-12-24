# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/api/domain/test/test_children.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.api.domain.children}.
"""
from twisted.trial import unittest
from spamfighter.api.domain.children import DomainChildrenCommand
from spamfighter.core.commands.partner import PartnerAuthInfo

class DomainChildrenCommandTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.domain.children.DomainChildrenCommand}.
    """

    def testRun(self):
        c = DomainChildrenCommand()
        c.params.partner = PartnerAuthInfo(None)
        return c.run().addCallback(lambda _: self.assertEqual(c.result.children, []))