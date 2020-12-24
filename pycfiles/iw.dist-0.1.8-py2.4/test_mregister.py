# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/dist/tests/test_mregister.py
# Compiled at: 2008-03-20 05:18:16
"""Tests for distutils.command.register."""
import sys, os, unittest
from StringIO import StringIO
from iw.dist.mregister import mregister
from distutils.core import Distribution
from distutils.tests import support
from iw.dist.tests.test_pypirc import PYPIRC, PyPIRCCommandTestCase
import urllib2
data_sent = {}

class Opener(object):
    __module__ = __name__

    def open(self, req, data=None):
        if isinstance(req, str):
            assert req.startswith('http')
            return StringIO('ok')
        data_sent[req.get_host()] = (
         req.headers, req.data)


def build_opener(*auth):
    return Opener()


urllib2.build_opener = build_opener

class registerTestCase(PyPIRCCommandTestCase):
    __module__ = __name__

    def setUp(self):
        PyPIRCCommandTestCase.setUp(self)
        f = open(self.rc, 'w')
        f.write(PYPIRC)
        f.close()
        self.dist = Distribution()
        self.cmd = mregister(self.dist)

    def test_mregister(self):
        self.cmd.send_metadata()
        length = data_sent['pypi.python.org'][0]['Content-length']
        self.assertEquals(length, '1392')

    def test_get_non_default(self):
        self.cmd.repository = 'server2'
        self.cmd.send_metadata()
        self.assert_('another.pypi' in data_sent)
        import urllib2
        old = urllib2.HTTPPasswordMgr

        class _HTTPPasswordMgr:
            __module__ = __name__

            def add_password(self, realm, *args):
                urllib2._realm = realm

        urllib2.HTTPPasswordMgr = _HTTPPasswordMgr
        self.cmd.repository = 'server2'
        self.cmd.send_metadata()
        self.assert_('another.pypi' in data_sent)
        self.assertEquals(urllib2._realm, 'acme')
        urllib2.HTTPPasswordMgr = old
        delattr(urllib2, '_realm')

    def test_not_existing(self):
        self.cmd.repository = 'server128'
        self.assertRaises(ValueError, self.cmd.send_metadata)

    def test_creating_pypirc(self):
        os.remove(self.cmd._get_rc_file())
        self.cmd.repository = 'pypi'

        def _raw_input(msg=''):
            if msg == 'Save your login (y/N)?':
                return 'y'
            return '1'

        import getpass
        getpass.getpass = _raw_input
        func_globs = self.cmd.send_metadata.im_func.func_globals
        func_globs['raw_input'] = _raw_input
        self.cmd.send_metadata()
        content = open(self.cmd._get_rc_file()).read()
        content = content.replace(' ', '')
        wanted = ('        [pypirc]\n        servers = \n            pypi\n                \n        [pypi]\n        username:1\n        password:1').strip()
        self.assertEquals(content.strip(), wanted.replace(' ', ''))

    def test_classifiers(self):
        self.cmd.repository = 'server1'
        self.cmd.classifiers()


def test_suite():
    return unittest.makeSuite(registerTestCase)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')