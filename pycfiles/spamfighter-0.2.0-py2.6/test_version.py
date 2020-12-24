# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/api/info/test/test_version.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.api.info.version}.
"""
from twisted.trial import unittest
from spamfighter.api.info.version import InfoVersionCommand

class InfoVersionTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.api.info.version.InfoVersionCommand}.
    """

    def testRun(self):
        from spamfighter import version
        c = InfoVersionCommand()
        return c.run().addCallback(lambda _: self.assertEqual(version, c.result.version))