# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/modules/nl_sql.py
# Compiled at: 2011-01-18 18:36:28
"""
Load input into the Generic NL schema
See http://www.sqlalchemy.org/ for details on SQLAlchemy
"""
__rcsid__ = '$Id: nl_sql.py 26983 2011-01-18 23:36:28Z dang $'
__author__ = 'Monte Goode'
from netlogger import nlapi, nllog
from netlogger import util
from netlogger.analysis.schema.nl_schema import init_db
from netlogger.analysis.schema.nl_schema import Event, Identifier, Value
from netlogger.analysis.modules._base import Analyzer as BaseAnalyzer
from netlogger.analysis.modules._base import SQLAlchemyInit
from sqlalchemy.sql import functions
import sys, time

class Analyzer(BaseAnalyzer, SQLAlchemyInit):
    """Load into a generic SQL schema through SQLAlchemy.
    
    Parameters:
      - dsn {string,Required*}: SQLAlchemy connection string.
        The general form of this is 
          'dialect+driver://username:password@host:port/database'.
        See the SQLAlchemy docs for details.
        For sqlite, use 'sqlite:///foo.db' for a relative path and
        'sqlite:////path/to/foo.db' (four slashes) for an absolute one.
     - batch_len {int,50*}: Max length of batch to insert
     - batch_sec {int,1*}: Max seconds between batch inserts
    """

    def __init__(self, dsn=None, batch_len=50, batch_sec=1, perf='no', **kw):
        """Constructor.
        """
        BaseAnalyzer.__init__(self, **kw)
        self.log.info('init.start')
        if dsn is None:
            self.log.error('init.end', status=-1, msg='no dsn')
            raise ValueError('dsn is required')
        SQLAlchemyInit.__init__(self, dsn, init_db)
        self._bmaxlen, self._bsec = batch_len, batch_sec
        self._btime, self._blen = time.time(), 0
        self._perf = util.as_bool(perf)
        if self._perf:
            (self._insert_time, self._insert_num) = (0, 0)
        self.log.info('init.end')
        return

    def process(self, data):
        """Process the data
        """
        event = data.get('event', None)
        if event is None:
            self.log.error('process.end', status=-1)
            raise ValueError('Missing event')
        ts = data.get('ts', None)
        if ts is None:
            raise ValueError('Missing timestamp (ts)')
        if isinstance(ts, str):
            try:
                ts = float(ts)
            except ValueError:
                try:
                    ts = nlapi.parseISO(ts)
                except nlapi.DateFormatError:
                    raise ValueError("Bad timestamp '%s'" % ts)

        level_name = data.get('level', 'Info')
        level = nlapi.Level.names.get(level_name, nlapi.Level.INFO)
        if event.endswith('.start'):
            startend = 0
        elif event.endswith('.end'):
            startend = 1
        else:
            startend = 2
        status = data.get('status', None)
        if status is not None:
            try:
                status = int(status)
            except ValueError:
                raise "Bad status '%s'" % status

        if self._perf:
            t0 = time.time()
        eobj = Event()
        eobj.ts = ts
        eobj.event = event
        eobj.level = level
        eobj.startend = startend
        eobj.status = status
        self.session.add(eobj)
        for (k, v) in data.iteritems():
            if k.endswith('.id') or k == 'guid':
                item = Identifier()
                item.name, item.value = k, v
                eobj.identifiers.append(item)
            elif k not in ('event', 'ts', 'level', 'status'):
                item = Value()
                item.name, item.value = k, v
                eobj.values.append(item)

        self._blen += 1
        t = time.time()
        if self._perf:
            self._insert_time += t - t0
            self._insert_num += 1
        if self._blen >= self._bmaxlen or t - self._btime >= self._bsec:
            self._commit()
            self._blen, self._btime = 0, t
        return

    def finish(self):
        if self._perf:
            t0 = time.time()
        self._commit()
        if self._perf:
            self._insert_time += time.time() - t0
            self.log.info('performance', insert_time=self._insert_time, insert_num=self._insert_num, mean_time=self._insert_time / self._insert_num)

    def _commit(self):
        self.session.commit()