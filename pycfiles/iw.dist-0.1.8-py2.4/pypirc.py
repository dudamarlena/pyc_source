# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/dist/pypirc.py
# Compiled at: 2008-03-20 05:18:16
"""distutils.pypirc

Provides the PyPIRcCommand class, the base class for the command classes
that uses .pypirc in the distutils.command package.
"""
import os, sys
from ConfigParser import ConfigParser
from distutils.core import Command
DEFAULT_PYPIRC = '[pypirc]\nservers = \n    pypi\n    \n[pypi]\nusername:%s\npassword:%s\n'

class PyPIRCCommand(Command):
    """Base command that knows how to handle the .pypirc file
    """
    __module__ = __name__
    DEFAULT_REPOSITORY = 'http://pypi.python.org/pypi'
    DEFAULT_REALM = 'pypi'
    repository = None
    realm = None

    def _get_rc_file(self):
        """Returns rc file path."""
        return os.path.join(self._get_home(), '.pypirc')

    def _get_home(self):
        """Returns the home directory.
        
        home can differ depending on the platform"""
        home = os.getenv('HOME')
        if home is None:
            home_drive = os.getenv('HOMEDRIVE')
            home_path = os.getenv('HOMEPATH')
            if home_drive is not None and home_path is not None:
                return home_drive + home_path
        else:
            return home
        return os.curdir

    def _store_pypirc(self, username, password):
        """Creates a default .pypirc file."""
        rc = self._get_rc_file()
        f = open(rc, 'w')
        try:
            f.write(DEFAULT_PYPIRC % (username, password))
        finally:
            f.close()
        try:
            os.chmod(rc, 384)
        except OSError:
            pass

    def _read_pypirc(self):
        """Reads the .pypirc file."""
        rc = self._get_rc_file()
        if os.path.exists(rc):
            print 'Using PyPI login from %s' % rc
            repository = self.repository or self.DEFAULT_REPOSITORY
            realm = self.realm or self.DEFAULT_REALM
            config = ConfigParser()
            config.read(rc)
            sections = config.sections()
            if 'distutils' in sections:
                index_servers = config.get('distutils', 'index-servers')
                _servers = [ server.strip() for server in index_servers.split('\n') if server.strip() != '' ]
                if _servers == []:
                    if 'pypi' in sections:
                        _servers = [
                         'pypi']
                    else:
                        return {}
                for server in _servers:
                    current = {'server': server}
                    current['username'] = config.get(server, 'username')
                    current['password'] = config.get(server, 'password')
                    for (key, default) in (('repository', self.DEFAULT_REPOSITORY), ('realm', self.DEFAULT_REALM)):
                        if config.has_option(server, key):
                            current[key] = config.get(server, key)
                        else:
                            current[key] = default

                    if current['server'] == repository or current['repository'] == repository:
                        return current

            elif 'server-login' in sections:
                server = 'server-login'
                if config.has_option(server, 'repository'):
                    repository = config.get(server, 'repository')
                else:
                    repository = self.DEFAULT_REPOSITORY
                return {'username': config.get(server, 'username'), 'password': config.get(server, 'password'), 'repository': repository, 'server': server, 'realm': self.DEFAULT_REALM}
        return {}

    def initialize_options(self):
        self.repository = None
        self.realm = None
        return

    def finalize_options(self):
        if '-r' in sys.argv or '--repository' in sys.argv:
            if '-r' in sys.argv:
                pos = sys.argv.index('-r') + 1
            else:
                pos = sys.argv.index('--repository') + 1
            if len(sys.argv) > pos:
                self.repository = sys.argv[pos]
        if self.repository is None:
            self.repository = self.DEFAULT_REPOSITORY
        if self.realm is None:
            self.realm = self.DEFAULT_REALM
        return