# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/tango/test/tgtestds.py
# Compiled at: 2019-08-19 15:09:29
"""Module containing base classes for using the TangoSchemeTest DS in tests"""
from builtins import object
import PyTango
from taurus.core.tango.starter import ProcessStarter
from taurus.test import getResourcePath
__all__ = [
 'TangoSchemeTestLauncher']
__docformat__ = 'restructuredtext'

class TangoSchemeTestLauncher(object):
    """A base class for TestCase classes wishing to start a TangoSchemeTest.
    Use it as a mixin class"""
    DEV_NAME = 'TangoSchemeTest/unittest/temp-1'

    @classmethod
    def setUpClass(cls):
        """ Create and run a TangoSchemeTest device server
        """
        device = getResourcePath('taurus.core.tango.test.res', 'TangoSchemeTest')
        cls._starter = ProcessStarter(device, 'TangoSchemeTest/unittest')
        cls._starter.addNewDevice(cls.DEV_NAME, klass='TangoSchemeTest')
        cls._starter.startDs()

    @classmethod
    def tearDownClass(cls):
        """ Stop the device server and undo changes to the database
        """
        d = PyTango.DeviceProxy(cls.DEV_NAME)
        d.Reset()
        cls._starter.stopDs(hard_kill=True)
        cls._starter.cleanDb(force=True)

    def tearDown(self):
        d = PyTango.DeviceProxy(self.DEV_NAME)
        d.Reset()


if __name__ == '__main__':
    pass