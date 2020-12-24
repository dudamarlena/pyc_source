# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/tests/test_repos.py
# Compiled at: 2010-08-08 03:18:44
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pysvnmanager.lib.base import *
from pysvnmanager.tests import *
from pysvnmanager import model
from pysvnmanager.model import repos
from pysvnmanager.model import hooks
from pysvnmanager.hooks import plugins
import pylons.test, StringIO
from pprint import pprint

class TestRepos(TestController):

    def __init__(self, *args):
        wsgiapp = pylons.test.pylonsapp
        config = wsgiapp.config
        self.repos_root = config.get('repos_root', '') % {'here': config.get('here')}
        self.repos = repos.Repos(self.repos_root)
        super(TestRepos, self).__init__(*args)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReposCreate(self):
        self.assertRaises(Exception, self.repos.create, 'repos3')
        try:
            self.repos.delete('repos3')
            self.repos.create('repos3')
            self.assert_(sorted(self.repos.repos_list) == ['project1', 'project2', 'repos3'], self.repos.repos_list)
        except ImportError:
            pass

    def testReposDelete(self):
        try:
            self.repos.delete('project1')
        except Exception, e:
            self.assert_(str(e) == 'Repos project1 is not a blank repository.', str(e))

    def testReposRoot(self):
        repos.Repos('/tmp')
        self.assertRaises(Exception, repos.Repos, '/tmp/svnroot.noexists')

    def testReposlist(self):
        self.assert_(sorted(self.repos.repos_list) == ['project1', 'project2', 'repos3'], (',').join(self.repos.repos_list).encode('utf-8'))

    def testSvnVersion(self):
        svnversion = self.repos.svnversion()
        self.assert_(svnversion[0] != '', svnversion[0])
        self.assert_(svnversion[1] != '', svnversion[1])


class TestReposPlugin(TestController):

    def __init__(self, *args):
        wsgiapp = pylons.test.pylonsapp
        config = wsgiapp.config
        self.repos_root = config.get('repos_root', '') % {'here': config.get('here')}
        super(TestReposPlugin, self).__init__(*args)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testPluginList(self):
        self.assert_('CaseInsensitive' in plugins.modules, plugins.modules)
        self.assert_('EolStyleCheck' in plugins.modules, plugins.modules)

    def testPluginImport(self):
        self.assertRaises(Exception, plugins.getHandler('CaseInsensitive'), '')
        module_ci = plugins.getHandler('CaseInsensitive')(self.repos_root + '/project1')
        self.assert_(module_ci.name == 'Detect case-insensitive filename clashes', module_ci.name)
        self.assert_(module_ci.description != '', module_ci.description)

    def testPluginSetting(self):
        m = plugins.getHandler('CaseInsensitive')(self.repos_root + '/project1')
        self.assert_(m.enabled() == False)
        m.install()
        self.assert_(m.enabled() == True)
        m.uninstall()
        self.assert_(m.enabled() == False)

    def testHooks(self):
        self.assertRaises(AssertionError, hooks.Hooks, self.repos_root)
        myhooks = hooks.Hooks(self.repos_root + '/project1')
        self.assert_('CaseInsensitive' in myhooks.pluginnames, myhooks.pluginnames)
        self.assert_('EolStyleCheck' in myhooks.pluginnames, myhooks.pluginnames)
        self.assert_('CaseInsensitive' in myhooks.unapplied_plugins, myhooks.unapplied_plugins)
        self.assert_('EolStyleCheck' in myhooks.unapplied_plugins, myhooks.unapplied_plugins)
        m = myhooks.plugins['CaseInsensitive']
        self.assert_(m.name == 'Detect case-insensitive filename clashes', m.name)
        self.assert_(m.description != '', m.description)

    def testHooksSetting(self):
        myhooks = hooks.Hooks(self.repos_root + '/project1')
        m = myhooks.plugins['CaseInsensitive']
        self.assert_(m.enabled() == False)
        self.assert_('CaseInsensitive' not in myhooks.applied_plugins, myhooks.applied_plugins)
        self.assert_('EolStyleCheck' not in myhooks.applied_plugins, myhooks.applied_plugins)
        self.assert_('CaseInsensitive' in myhooks.unapplied_plugins, myhooks.unapplied_plugins)
        self.assert_('EolStyleCheck' in myhooks.unapplied_plugins, myhooks.unapplied_plugins)
        m.install()
        self.assert_(m.enabled() == True)
        self.assert_('CaseInsensitive' in myhooks.applied_plugins, myhooks.applied_plugins)
        self.assert_('EolStyleCheck' not in myhooks.applied_plugins, myhooks.applied_plugins)
        self.assert_('CaseInsensitive' not in myhooks.unapplied_plugins, myhooks.unapplied_plugins)
        self.assert_('EolStyleCheck' in myhooks.unapplied_plugins, myhooks.unapplied_plugins)
        m.uninstall()
        self.assert_(m.enabled() == False)
        self.assert_('CaseInsensitive' not in myhooks.applied_plugins, myhooks.applied_plugins)
        self.assert_('EolStyleCheck' not in myhooks.applied_plugins, myhooks.applied_plugins)
        self.assert_('CaseInsensitive' in myhooks.unapplied_plugins, myhooks.unapplied_plugins)
        self.assert_('EolStyleCheck' in myhooks.unapplied_plugins, myhooks.unapplied_plugins)


if __name__ == '__main__':
    import unittest
    unittest.main()