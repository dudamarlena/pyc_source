# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/modules/couchdb.py
# Compiled at: 2010-09-20 13:45:35
"""
Load input in to a CouchDB database

See http://couchdb.apache.org for CouchDB
See http://couchdbkit.org for the Python API details
"""
import sys, time, couchdbkit
from netlogger.analysis.modules._base import Analyzer as BaseAnalyzer
from netlogger.analysis.modules._base import ConnectionException
from netlogger import util

class Analyzer(BaseAnalyzer):
    """Load records into a CouchDB database. !!EXPERIMENTAL!!

    Parameters: 
      - host {string,localhost*}: Server host
      - port {integer,5984*}: Server port
      - database {string,application*}: Name of database to create/use
      - batch_size {integer,1*}: Number of records to 'batch up' for
        one insert. A value of 0 or 1 means insert each record as it comes.
        For high-throughput, a large number like 10000 is appropriate.
      - batch_sec {float,0*}: If batch_size is greater than 1, this is
        the maximum amount of time between (batch) inserts when the data
        is continuously flowing. Note that interruptions in the input may
        cause the last partial batch of items to wait indefinitely.
        A value less than or equal to zero means to ignore this parameter.
    """

    def __init__(self, host='localhost', port=5984, database='application', batch_size=1, batch_sec=0, perf='no', **kw):
        BaseAnalyzer.__init__(self, **kw)
        url = 'http://%s:%d' % (host, port)
        self._server = couchdbkit.Server(url)
        try:
            self._server.info()
        except couchdbkit.RequestFailed:
            raise ConnectionException('Connection failed to CouchDB server running on %s:%d' % (
             host, port))

        self._db = self._server.get_or_create_db(database)
        try:
            batch_size = int(batch_size)
            if batch_size < 1:
                raise ValueError()
        except ValueError:
            raise ValueError('Illegal batch_size')

        try:
            batch_sec = float(batch_sec)
        except ValueError:
            raise ValueError('Illegal batch_sec')

        if batch_size > 1:
            self._batch = Batch(batch_size, batch_sec)
        else:
            self._batch = None
        self._perf = util.as_bool(perf)
        if self._perf:
            (self._insert_time, self._insert_num) = (0, 0)
        return

    def fix_key_formats(self, data):
        """Make sure key names are not illegal
        * cannot have a '.' anywhere will replace with '_'
        * cannot have $ as first symbol will remove
        """
        fixed_data = {}
        for (key, value) in data.items():
            if '.' in key:
                key = key.replace('.', '_')
            if key[0] == '$':
                key = key.lstrip('$')
            fixed_data[key] = value

        return fixed_data

    def process(self, data):
        """Insert 'data' into database
        """
        if self._dbg:
            self.log.debug('process_data.start')
        data = self.fix_key_formats(data)
        if self._batch and self._batch.ready():
            if self._perf:
                t = time.time()
                items = self._batch.get_all()
                self._db.bulk_save(items)
                self._insert_time += time.time() - t
                self._insert_num += len(items)
            else:
                self._db.bulk_save(self._batch.get_all())
        if data.has_key('status'):
            try:
                data['status'] = int(data['status'])
            except ValueError:
                self.log.warn('bad_status', value=data['status'], msg='not integer')

        data['_id'] = util.uuid1()
        self._insert(data)
        if self._dbg:
            self.log.debug('process_data.end')

    def _insert(self, data):
        """Insert data by either adding to batch or really
        inserting it into the datbase.
        """
        if self._batch:
            self._batch.add(data)
        elif self._perf:
            t = time.time()
            doc = self._db.save_doc(data)
            self._insert_time += time.time() - t
            self._insert_num += 1
        else:
            doc = self._db.save_doc(data)

    def finish(self):
        """Print perf on cleanup. Only shown if
        verbosity is at 'INFO' (one -v) or above.
        """
        if self._batch:
            if self._perf:
                t = time.time()
                items = self._batch.get_all()
                self._db.bulk_save(items)
                self._insert_time += time.time() - t
                self._insert_num += len(items)
            else:
                self._db.bulk_save(self._batch.get_all())
        if self._perf:
            self.log.info('performance', insert_time=self._insert_time, insert_num=self._insert_num, mean_time=self._insert_time / self._insert_num)


class Batch:
    """Batch of items with a timeout.
    """

    def __init__(self, size, timeout):
        """Ctor.
        'size' is the max. number of items in the batch
        'timeout' is a timeout in seconds, after which the batch
                  is considered "ready" even if it is not full
        """
        self._items = []
        self._size = size
        self._timeout = max(timeout, 0)
        self._start_time = None
        return

    def add(self, item):
        """Add an item to the batch.
        """
        if not self._items:
            self._start_time = time.time()
        self._items.append(item)

    def ready(self):
        """Return True if the batch is ready to be emptied,
        according to its size and the current time.
        """
        if not self._items:
            res = False
        elif len(self._items) >= self._size:
            res = True
        elif self._timeout > 0 and time.time() - self._start_time >= self._timeout:
            res = True
        else:
            res = False
        return res

    def get_all(self):
        """Return and clear the batch.
        """
        copy = self._items
        self._items, self._start_time = [], None
        return copy