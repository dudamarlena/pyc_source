# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/tests/base.py
# Compiled at: 2008-10-23 05:55:15
"""Defines a test class and its Plone Site layer for plone tests"""
import os, Globals
from Testing import ZopeTestCase as ztc
from zope.interface import classImplements
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.CMFPlone.Portal import PloneSite
from Products.CMFPlone.interfaces import ITestCasePloneSiteRoot
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite as PloneSiteLayer
from Products.PloneTestCase.layer import onsetup
classImplements(PloneSite, ITestCasePloneSiteRoot)
STORAGE_PATH = os.path.join(Globals.INSTANCE_HOME, 'var', 'unittests_storage')
BACKUP_PATH = os.path.join(Globals.INSTANCE_HOME, 'var', 'unittests_backup')

@onsetup
def setup_fss():
    """Set up the additional products required for fss.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    import iw.fss
    iw.fss.customconfig.ZOPETESTCASE = True
    from iw.fss.customconfig import INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE
    os.environ[INSTALL_EXAMPLE_TYPES_ENVIRONMENT_VARIABLE] = 'True'
    ztc.installPackage('iw.fss')


def createTemporaryDirs():
    for base_path in (STORAGE_PATH, BACKUP_PATH):
        if not os.path.exists(base_path):
            os.mkdir(base_path)


def removeTemporaryDirs():
    import shutil
    shutil.rmtree(STORAGE_PATH)
    shutil.rmtree(BACKUP_PATH)


setup_fss()
ptc.setupPloneSite(products=['iw.fss'], extension_profiles=['iw.fss:default', 'iw.fss:testfixtures'])
from Products.MailHost import MailHost

class TestMailHost(MailHost.MailHost):
    __module__ = __name__

    def _send(self, mfrom, mto, messageText):
        """Fake sender"""
        print messageText


class TestCase(ptc.FunctionalTestCase):
    """test case used in tests"""
    __module__ = __name__

    class layer(PloneSiteLayer):
        __module__ = __name__

        @classmethod
        def setUp(cls):
            import iw.fss
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', iw.fss)
            fiveconfigure.debug_mode = False
            cls._old = MailHost.MailHost
            MailHost.MailHost = TestMailHost
            createTemporaryDirs()

        @classmethod
        def tearDown(cls):
            MailHost.MailHost = cls._old
            removeTemporaryDirs()