# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\barfeed\sqlitefeed.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 6039 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade.barfeed import dbfeed
from pyalgotrade.barfeed import membf
from pyalgotrade import bar
from pyalgotrade.utils import dt
import sqlite3, os

def normalize_instrument(instrument):
    return instrument.upper()


class Database(dbfeed.Database):

    def __init__(self, dbFilePath):
        self._Database__instrumentIds = {}
        initialize = False
        if not os.path.exists(dbFilePath):
            initialize = True
        self._Database__connection = sqlite3.connect(dbFilePath)
        self._Database__connection.isolation_level = None
        if initialize:
            self.createSchema()

    def __findInstrumentId(self, instrument):
        cursor = self._Database__connection.cursor()
        sql = 'select instrument_id from instrument where name = ?'
        cursor.execute(sql, [instrument])
        ret = cursor.fetchone()
        if ret is not None:
            ret = ret[0]
        cursor.close()
        return ret

    def __addInstrument(self, instrument):
        ret = self._Database__connection.execute('insert into instrument (name) values (?)', [instrument])
        return ret.lastrowid

    def __getOrCreateInstrument(self, instrument):
        ret = self._Database__instrumentIds.get(instrument, None)
        if ret is not None:
            return ret
        ret = self._Database__findInstrumentId(instrument)
        if ret is None:
            ret = self._Database__addInstrument(instrument)
        self._Database__instrumentIds[instrument] = ret
        return ret

    def createSchema(self):
        self._Database__connection.execute('create table instrument (instrument_id integer primary key autoincrement, name text unique not null)')
        self._Database__connection.execute('create table bar (instrument_id integer references instrument (instrument_id), frequency integer not null, timestamp integer not null, open real not null, high real not null, low real not null, close real not null, volume real not null, adj_close real, primary key (instrument_id, frequency, timestamp))')

    def addBar(self, instrument, bar, frequency):
        instrument = normalize_instrument(instrument)
        instrumentId = self._Database__getOrCreateInstrument(instrument)
        timeStamp = dt.datetime_to_timestamp(bar.getDateTime())
        try:
            sql = 'insert into bar (instrument_id, frequency, timestamp, open, high, low, close, volume, adj_close) values (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            params = [instrumentId, frequency, timeStamp, bar.getOpen(), bar.getHigh(), bar.getLow(), bar.getClose(), bar.getVolume(), bar.getAdjClose()]
            self._Database__connection.execute(sql, params)
        except sqlite3.IntegrityError:
            sql = 'update bar set open = ?, high = ?, low = ?, close = ?, volume = ?, adj_close = ? where instrument_id = ? and frequency = ? and timestamp = ?'
            params = [
             bar.getOpen(), bar.getHigh(), bar.getLow(), bar.getClose(), bar.getVolume(), bar.getAdjClose(), instrumentId, frequency, timeStamp]
            self._Database__connection.execute(sql, params)

    def getBars(self, instrument, frequency, timezone=None, fromDateTime=None, toDateTime=None):
        instrument = normalize_instrument(instrument)
        sql = 'select bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume, bar.adj_close, bar.frequency from bar join instrument on (bar.instrument_id = instrument.instrument_id) where instrument.name = ? and bar.frequency = ?'
        args = [
         instrument, frequency]
        if fromDateTime is not None:
            sql += ' and bar.timestamp >= ?'
            args.append(dt.datetime_to_timestamp(fromDateTime))
        if toDateTime is not None:
            sql += ' and bar.timestamp <= ?'
            args.append(dt.datetime_to_timestamp(toDateTime))
        sql += ' order by bar.timestamp asc'
        cursor = self._Database__connection.cursor()
        cursor.execute(sql, args)
        ret = []
        for row in cursor:
            dateTime = dt.timestamp_to_datetime(row[0])
            if timezone:
                dateTime = dt.localize(dateTime, timezone)
            ret.append(bar.BasicBar(dateTime, row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

        cursor.close()
        return ret

    def disconnect(self):
        self._Database__connection.close()
        self._Database__connection = None


class Feed(membf.BarFeed):

    def __init__(self, dbFilePath, frequency, maxLen=None):
        super(Feed, self).__init__(frequency, maxLen)
        self._Feed__db = Database(dbFilePath)

    def barsHaveAdjClose(self):
        return True

    def getDatabase(self):
        return self._Feed__db

    def loadBars(self, instrument, timezone=None, fromDateTime=None, toDateTime=None):
        bars = self._Feed__db.getBars(instrument, self.getFrequency(), timezone, fromDateTime, toDateTime)
        self.addBarsFromSequence(instrument, bars)