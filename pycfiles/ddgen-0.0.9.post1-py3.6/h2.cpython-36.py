# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ddgen/db/h2.py
# Compiled at: 2020-03-31 14:41:06
# Size of source mod 2**32: 4356 bytes
import logging, os, subprocess, time, psycopg2 as pg
from pkg_resources import resource_filename
h2_jar = resource_filename(__name__, 'jar/h2-1.4.199.jar')
default_h2_version = '1.4.200'
supported_h2_versions = ('1.4.199', '1.4.200')

class H2DbManager:

    def __init__(self, db_path: str, user: str, password: str, host: str='localhost', port: str='65435', h2_version='1.4.200'):
        """Create H2 manager using provided H2 database file and credentials.

        :param db_path: path to database file
        :param user: user name
        :param password: password to use
        :param host: host address
        :param port: port in usage
        :param h2_version: H2 version to use, choose from {1.4.199, 1.4.200}
        """
        self._logger = logging.getLogger(__name__)
        self._db_dir, self._db_filename = self.split_db_path(db_path)
        self._user = user
        self._passwd = password
        self._host = host
        self._port = port
        self._url = ''
        self._cp = None
        if h2_version not in supported_h2_versions:
            self._logger.warning('H2 version `{}` not supported. Falling back to {}'.format(h2_version, default_h2_version))
            self._h2_version = default_h2_version
        else:
            self._h2_version = h2_version
        self._h2_jar = resource_filename(__name__, 'jar/h2-{}.jar'.format(self._h2_version))
        self._perform_checks()

    def __enter__(self):
        """Spool up H2 server."""
        self.spool_up_server()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Shut down the H2 server process."""
        self.shut_down_server()

    def __repr__(self):
        return 'H2DbManager({}, user={}, password={}, host={}, port={})'.format(os.path.join(self._db_dir, self._db_filename) + '.mv.db', self._user, self._passwd, self._host, self._port)

    def spool_up_server(self):
        """Spool up H2 server."""
        self._url = '{}:{}'.format(self._host, self._port)
        self._logger.info("Spooling up H2 server at '{}'".format(self._url))
        self._cp = subprocess.Popen(('java', '-cp', h2_jar, 'org.h2.tools.Server',
         '-pg', '-baseDir', self._db_dir, '-pgPort', self._port))
        time.sleep(1)

    def shut_down_server(self):
        """Shut down the H2 server process."""
        self._logger.info("Shutting down the H2 server at '{}'".format(self._url))
        self._cp.terminate()
        return_code = self._cp.wait()
        self._logger.info('Server returned {}'.format(return_code))

    def get_connection(self):
        """Return a new connection to the database."""
        if not self._cp:
            raise H2DbException('Cannot get connection to the database before spooling up H2 server. Call `spool_up_server` method first')
        cstring = "dbname={} user={} password='{}' host={} port={}".format(self._db_filename, self._user, self._passwd, self._host, self._port)
        return pg.connect(cstring)

    def _perform_checks(self):
        """Perform sanity checks. An exception is raised here if anything is wrong to ensure an early failure."""
        if not self.check_java_is_in_system():
            raise H2DbException('Java executable was not found on the local system')

    @staticmethod
    def split_db_path(db_path: str) -> tuple:
        if os.path.isfile(db_path):
            if db_path.endswith('.mv.db'):
                db_path = db_path[:-6]
            return os.path.split(db_path)
        raise H2DbException("'{}' does not point to a file".format(db_path))

    @staticmethod
    def check_java_is_in_system():
        process = subprocess.run(('which', 'java'))
        return process.returncode == 0


class H2DbException(Exception):
    pass