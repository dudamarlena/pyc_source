# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/dist/tests/test_pypirc.py
# Compiled at: 2008-03-20 05:18:16
"""Tests for distutils.pypirc.pypirc."""
import sys, os, unittest
from iw.dist.core import PyPIRCCommand
from distutils.core import Distribution
from distutils.tests import support
PYPIRC = '[distutils]\n\nindex-servers = \n    server1\n    server2\n\n[server1]\nusername:me\npassword:secret\n\n[server2]\nusername:meagain\npassword: secret\nrealm:acme\nrepository:http://another.pypi/\n'
PYPIRC_OLD = '[server-login]\nusername:tarek\npassword:secret\n'

class PyPIRCCommandTestCase(support.TempdirManager, unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        """Patches the environment."""
        if os.environ.has_key('HOME'):
            self._old_home = os.environ['HOME']
        else:
            self._old_home = None
        curdir = os.path.dirname(__file__)
        os.environ['HOME'] = curdir
        self.rc = os.path.join(curdir, '.pypirc')
        self.dist = Distribution()

        class command(PyPIRCCommand):
            __module__ = __name__

            def __init__(self, dist):
                PyPIRCCommand.__init__(self, dist)

            def initialize_options(self):
                pass

            finalize_options = initialize_options

        self._cmd = command
        return

    def tearDown(self):
        """Removes the patch."""
        if self._old_home is None:
            del os.environ['HOME']
        else:
            os.environ['HOME'] = self._old_home
        if os.path.exists(self.rc):
            os.remove(self.rc)
        return

    def test_server_registration(self):
        f = open(self.rc, 'w')
        try:
            f.write(PYPIRC)
        finally:
            f.close()
        cmd = self._cmd(self.dist)
        config = cmd._read_pypirc()
        config = config.items()
        config.sort()
        waited = [('password', 'secret'), ('realm', 'pypi'), ('repository', 'http://pypi.python.org/pypi'), ('server', 'server1'), ('username', 'me')]
        self.assertEquals(config, waited)
        f = open(self.rc, 'w')
        f.write(PYPIRC_OLD)
        f.close()
        config = cmd._read_pypirc()
        config = config.items()
        config.sort()
        waited = [('password', 'secret'), ('realm', 'pypi'), ('repository', 'http://pypi.python.org/pypi'), ('server', 'server-login'), ('username', 'tarek')]
        self.assertEquals(config, waited)

    def test_get_home(self):
        cmd = self._cmd(self.dist)
        curdir = os.path.dirname(__file__)
        self.assertEquals(cmd._get_home(), curdir)
        del os.environ['HOME']
        os.environ['HOMEPATH'] = os.path.dirname(__file__)
        os.environ['HOMEDRIVE'] = 'the_drive'
        self.assertEquals(cmd._get_home(), 'the_drive' + curdir)
        del os.environ['HOMEDRIVE']
        del os.environ['HOMEPATH']
        self.assertEquals(cmd._get_home(), os.curdir)
        os.environ['HOME'] = curdir

    def test_repository_in_args(self):
        sys.argv.extend(['-r', 'toto'])
        try:
            cmd = PyPIRCCommand(self.dist)
            cmd.finalize_options()
            self.assertEquals(cmd.repository, 'toto')
        finally:
            sys.argv = sys.argv[:-2]


def test_suite():
    return unittest.makeSuite(PyPIRCCommandTestCase)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')