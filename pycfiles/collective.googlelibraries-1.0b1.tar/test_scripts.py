# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/toutpt/workspace/collective.googlelibraries/collective/googlelibraries/tests/test_scripts.py
# Compiled at: 2010-12-01 19:06:44
import unittest
from collective.googlelibraries import scripts
from collective.googlelibraries.tests import base

class Test(base.TestCase):

    def afterSetUp(self):
        self.view = scripts.ScriptsView(self.portal, self.portal.REQUEST)

    def test_nojsapi(self):
        scripts = self.view.scripts()
        srcs = [ script['src'] for script in scripts ]
        for src in srcs:
            self.failUnless('jsapi' not in src)

    def test_jsapi(self):
        apikey = self.view.apikey_manager
        apikey.google_keys = ('http://nohost | ZZOOPPEE', )
        scripts = self.view.scripts()
        srcs = [ script['src'] for script in scripts if 'jsapi' in script['src'] ]
        self.failUnless(len(srcs) == 1)
        self.failUnless('jsapi' in scripts[0]['src'])

    def test_scripts(self):
        apikey = self.view.apikey_manager
        apikey.google_keys = ('http://nohost | ZZOOPPEE', )
        library = self.view.library_manager
        library.libraries = ('jquery | 1.4.4', )
        scripts = self.view.scripts()
        script = scripts[1]
        self.failUnless(script['src'] == 'https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js', script['src'])

    def test_googleapi(self):
        pass


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite