# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/base/tests/test_settings.py
# Compiled at: 2010-02-07 17:28:31
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
import unittest
from pyogp.lib.base.settings import Settings
import pyogp.lib.base.tests.config

class TestEvents(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_base_settings(self):
        settings = Settings()
        self.assertEquals(settings.quiet_logging, False)
        self.assertEquals(settings.HANDLE_PACKETS, True)
        self.assertEquals(settings.LOG_VERBOSE, True)
        self.assertEquals(settings.ENABLE_BYTES_TO_HEX_LOGGING, False)
        self.assertEquals(settings.ENABLE_CAPS_LOGGING, True)
        self.assertEquals(settings.ENABLE_CAPS_LLSD_LOGGING, False)
        self.assertEquals(settings.ENABLE_EQ_LOGGING, True)
        self.assertEquals(settings.ENABLE_UDP_LOGGING, True)
        self.assertEquals(settings.ENABLE_OBJECT_LOGGING, True)
        self.assertEquals(settings.LOG_SKIPPED_PACKETS, True)
        self.assertEquals(settings.ENABLE_HOST_LOGGING, True)
        self.assertEquals(settings.LOG_COROUTINE_SPAWNS, True)
        self.assertEquals(settings.DISABLE_SPAMMERS, True)
        self.assertEquals(settings.UDP_SPAMMERS, ['PacketAck', 'AgentUpdate'])

    def test_quiet_settings(self):
        settings = Settings(True)
        self.assertEquals(settings.quiet_logging, True)
        self.assertEquals(settings.HANDLE_PACKETS, True)
        self.assertEquals(settings.LOG_VERBOSE, False)
        self.assertEquals(settings.ENABLE_BYTES_TO_HEX_LOGGING, False)
        self.assertEquals(settings.ENABLE_CAPS_LOGGING, False)
        self.assertEquals(settings.ENABLE_CAPS_LLSD_LOGGING, False)
        self.assertEquals(settings.ENABLE_EQ_LOGGING, False)
        self.assertEquals(settings.ENABLE_UDP_LOGGING, False)
        self.assertEquals(settings.ENABLE_OBJECT_LOGGING, False)
        self.assertEquals(settings.LOG_SKIPPED_PACKETS, False)
        self.assertEquals(settings.ENABLE_HOST_LOGGING, False)
        self.assertEquals(settings.LOG_COROUTINE_SPAWNS, False)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestEvents))
    return suite