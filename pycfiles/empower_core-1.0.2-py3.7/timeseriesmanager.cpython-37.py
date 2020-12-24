# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/timeseriesmanager/timeseriesmanager.py
# Compiled at: 2020-05-10 06:48:23
# Size of source mod 2**32: 4837 bytes
"""Time series manager."""
from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from influxdb import InfluxDBClient
from empower_core.service import EService
import empower_core.serialize as serialize
DEFAULT_DATABASE = 'tsmanager'
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8086
DEFAULT_USERNAME = 'root'
DEFAULT_PASSWORD = 'password'

class InfluxTimeSeriesManager(EService):
    __doc__ = 'Time series manager.'

    def __init__(self, context, service_id, database, host, port, username, password):
        super().__init__(context=context, service_id=service_id, database=database,
          host=host,
          port=port,
          username=username,
          password=password)
        self.thread_pool = None
        self.influxdb_client = None
        self.stats = []
        self.busy = False

    def start(self):
        super().start()
        self.thread_pool = ThreadPoolExecutor(1)
        self.influxdb_client = InfluxDBClient(host=(self.host), port=(self.port),
          username=(self.username),
          password=(self.password),
          timeout=3,
          database=(self.database))
        try:
            self.influxdb_client.create_database(self.database)
            self.log.info('Connected to InfluxDB database %s', self.database)
        except Exception as ex:
            try:
                self.log.exception(ex)
            finally:
                ex = None
                del ex

    @property
    def database(self):
        """Return database."""
        return self.params['database']

    @database.setter
    def database(self, value):
        """Set database."""
        self.params['database'] = value

    @property
    def host(self):
        """Return host."""
        return self.params['host']

    @host.setter
    def host(self, value):
        """Set host."""
        self.params['host'] = value

    @property
    def port(self):
        """Return port."""
        return self.params['port']

    @port.setter
    def port(self, value):
        """Set port."""
        self.params['port'] = int(value)

    @property
    def username(self):
        """Return username."""
        return self.params['username']

    @username.setter
    def username(self, value):
        """Set username."""
        self.params['username'] = value

    @property
    def password(self):
        """Return password."""
        return self.params['password']

    @password.setter
    def password(self, value):
        """Set password."""
        self.params['password'] = value

    @gen.coroutine
    def write_points(self, points):
        """Add new points to the DB."""
        if self.busy:
            self.stats.append(points)
            return
        self.busy = True
        error = yield self.thread_pool.submit(self._InfluxTimeSeriesManager__write_points_worker, points)
        self.busy = False
        if error:
            self.stats.clear()
        if self.stats:
            self.write_points(self.stats.pop(0))

    def __write_points_worker(self, points):
        try:
            self.influxdb_client.write_points(points=(serialize(points)))
        except Exception as ex:
            try:
                self.log.exception(ex)
                return True
            finally:
                ex = None
                del ex

        return False


def launch(context, service_id, database=DEFAULT_DATABASE, host=DEFAULT_HOST, port=DEFAULT_PORT, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD):
    """ Initialize the module. """
    return InfluxTimeSeriesManager(context=context, service_id=service_id, database=database,
      host=host,
      port=port,
      username=username,
      password=password)