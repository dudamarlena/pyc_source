# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/tests/test_configuration.py
# Compiled at: 2008-10-23 05:55:15
"""
Testing configuration schema and default configuration file
$Id: test_configuration.py 66025 2008-06-02 13:53:50Z glenfant $
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
import unittest, os
from StringIO import StringIO
import ZConfig, iw.fss.customconfig
iw.fss.customconfig.ZOPETESTCASE = True
from iw.fss.configuration import datatypes
GOOD_CONFIG1 = '# Two distinct directories\nstorage-path $$INSTANCE_HOME/var\nbackup-path $$INSTANCE_HOME/etc\nstorage-strategy directory\n'
GOOD_CONFIG2 = '# Two distinct directories, two plone sites\nstorage-path $$INSTANCE_HOME/lib\nbackup-path $$INSTANCE_HOME/var\n# default storage-strategy (flat)\n<site /foo/bar>\n  storage-path $$INSTANCE_HOME/bin\n  backup-path $$INSTANCE_HOME/log\n  storage-strategy directory\n</site>\n<site /YO/stuff>\n  storage-path $$INSTANCE_HOME/etc\n  backup-path $$INSTANCE_HOME/Products\n  # default storage-strategy (flat)\n</site>\n'
GOOD_CONFIG3 = '# Empty config file ;-)\n# Assumes that $INSTANCE/var/fss_storage and $INSTANCE/var/fss_backup\n'
_good_configs = (
 GOOD_CONFIG1, GOOD_CONFIG2, GOOD_CONFIG3)
BAD_CONFIG1 = '# Non existing storage directory\nstorage-path /foo/bar\n'
BAD_CONFIG2 = '# No write access to storage directory (Unix)\nstorage-path /etc\n'
BAD_CONFIG3 = '# Duplicated directories\nstorage-path $$INSTANCE_HOME/var/fss_storage\nbackup-path $$INSTANCE_HOME/var/fss_storage\n'
BAD_CONFIG4 = '# No such strategy\nstorage-strategy foo\n'
BAD_CONFIG5 = '# site1 default strategy forbidden\nstorage-strategy site1'
_bad_configs = (
 BAD_CONFIG1, BAD_CONFIG2, BAD_CONFIG3, BAD_CONFIG4, BAD_CONFIG5)

class ConfigSchemaTest(unittest.TestCase):
    """Testing configuration schema conformance"""
    __module__ = __name__

    def testSchemaConformance(self):
        """Our schema.xml conforms ZConfig schema"""
        from iw.fss.configuration import schema
        self.schema = schema.fssSchema


class BaseConfigTest(unittest.TestCase):
    """Common resources for testing FSS configuration"""
    __module__ = __name__

    def setUp(self):
        from iw.fss.configuration import schema
        self.schema = schema.fssSchema


class ConfigFilesValidityTest(BaseConfigTest):
    """Testing some configuration files"""
    __module__ = __name__

    def testGoodConfigLoad(self):
        """A bunch of correct configuration files"""
        global _good_configs
        for config in _good_configs:
            good_config = StringIO(config)
            (conf, handler) = ZConfig.loadConfigFile(self.schema, good_config)
            datatypes._paths = []

    def testBadConfigLoad(self):
        """A bunch of incorrect configuration files"""
        global _bad_configs
        for config in _bad_configs:
            bad_config = StringIO(config)
            self.failUnlessRaises(Exception, ZConfig.loadConfigFile, self.schema, bad_config)
            datatypes._paths = []


class ConfigObjectTest(BaseConfigTest):
    """Testing configuration classes"""
    __module__ = __name__

    def setUp(self):
        super(ConfigObjectTest, self).setUp()
        (self.zconf, handler) = ZConfig.loadConfigFile(self.schema, StringIO(GOOD_CONFIG2))
        datatypes._paths = []

    def testGlobalAttrs(self):
        """Attributes of global config"""
        self.assertEqual(self.zconf.storage_path, os.path.expandvars('$INSTANCE_HOME/lib'))
        self.assertEqual(self.zconf.backup_path, os.path.expandvars('$INSTANCE_HOME/var'))
        self.assertEqual(self.zconf.storage_strategy, 'flat')
        self.assertEqual(len(self.zconf.sites), 2)

    def testSitesAttrs(self):
        """Attributes of site specific settings"""
        expected = {'storage_path': os.path.expandvars('$INSTANCE_HOME/bin'), 'backup_path': os.path.expandvars('$INSTANCE_HOME/log'), 'storage_strategy': 'directory', 'name': '/foo/bar'}
        self._testSiteAttrs(self.zconf.sites[0], expected)
        expected = {'storage_path': os.path.expandvars('$INSTANCE_HOME/etc'), 'backup_path': os.path.expandvars('$INSTANCE_HOME/Products'), 'storage_strategy': 'flat', 'name': '/YO/stuff'}
        self._testSiteAttrs(self.zconf.sites[1], expected)

    def _testSiteAttrs(self, siteconf, expected):
        for (attrname, value) in expected.items():
            if attrname == 'name':
                self.assertEqual(getattr(siteconf, attrname), value.lower())
            else:
                self.assertEqual(getattr(siteconf, attrname), value)

    def testConfigServices(self):
        """Canonical config API"""
        self.assertEqual(self.zconf.storagePathForSite('/any/site'), os.path.expandvars('$INSTANCE_HOME/lib'))
        self.assertEqual(self.zconf.backupPathForSite('/any/site'), os.path.expandvars('$INSTANCE_HOME/var'))
        self.assertEqual(self.zconf.storageStrategyForSite('/any/site'), 'flat')
        self.assertEqual(self.zconf.storagePathForSite('/foo/bar'), os.path.expandvars('$INSTANCE_HOME/bin'))
        self.assertEqual(self.zconf.backupPathForSite('/foo/bar'), os.path.expandvars('$INSTANCE_HOME/log'))
        self.assertEqual(self.zconf.storageStrategyForSite('/foo/bar'), 'directory')
        self.assertEqual(self.zconf.storagePathForSite('/YO/stuff'), os.path.expandvars('$INSTANCE_HOME/etc'))
        self.assertEqual(self.zconf.backupPathForSite('/YO/stuff'), os.path.expandvars('$INSTANCE_HOME/Products'))
        self.assertEqual(self.zconf.storageStrategyForSite('/YO/stuff'), 'flat')


class DefaultConfigTest(unittest.TestCase):
    """Checking the default configuration file
    (etc/plone-filesystemstorage.conf.in)"""
    __module__ = __name__

    def testDefaultConfig(self):
        from iw.fss.config import ZCONFIG
        self.assertEqual(ZCONFIG.storagePathForSite('/any/site'), os.path.normpath(os.path.expandvars('$INSTANCE_HOME/var/fss_storage')))
        self.assertEqual(ZCONFIG.backupPathForSite('/any/site'), os.path.normpath(os.path.expandvars('$INSTANCE_HOME/var/fss_backup')))
        self.assertEqual(ZCONFIG.storageStrategyForSite('/any/site'), 'flat')
        self.assertEqual(len(ZCONFIG.sites), 0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ConfigSchemaTest))
    suite.addTest(makeSuite(ConfigFilesValidityTest))
    suite.addTest(makeSuite(ConfigObjectTest))
    suite.addTest(makeSuite(DefaultConfigTest))
    return suite