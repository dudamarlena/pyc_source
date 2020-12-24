# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/timeseriesdatabasetest.py
# Compiled at: 2015-05-28 05:23:35
import unittest, random, sqlite3
from pycast.common.timeseries import TimeSeries, MultiDimensionalTimeSeries

class DatabaseConnectorTest(unittest.TestCase):
    """Testclass for all database connection related tests."""

    def setUp(self):
        """Initializes the environment for each test."""
        self._db = sqlite3.connect(':memory:')
        self.add_data_into_db(self._db, random.randint(100, 10000))

    def tearDown(self):
        """This function gets called after each test function."""
        self._db.close()
        del self._db

    def add_data_into_db(self, database, numberOfTuples):
        """Inserts a numberOfTuples tuples into the given database.

        This automatically creates a table called TestTable with the following schema:
            timestamp REAL
            value     REAL
            junk_one  REAL
            junk_two  TEXT

        The time stamps will be inserted as an ordered sequence.

        @param database dbapi2.connection Instance for the used database.
        @param numberOfTuples Number of tuples that have to be created.
        """
        cur = database.cursor()
        cur.execute('\n            CREATE TABLE TestTable(\n                timestamp REAL,\n                value     REAL,\n                junk_one  REAL,\n                junk_two  TEXT\n            )\n            ')
        database.commit()
        timestamp = 0
        junk_two = ['test']
        tuples = []
        append = tuples.append
        for item in xrange(numberOfTuples):
            timestamp += random.random()
            value = random.random() * 1000
            junkOne = random.random()
            junkTwo = random.choice(junk_two)
            append([timestamp, value, junkOne, junkTwo])

        cur.executemany('INSERT INTO TestTable VALUES (?,?,?,?)', tuples)
        database.commit()

    def select_to_many_attributes_test(self):
        """SELECT timestamp, value, junk, FROM TestTable

        This function tests if statements like 

        SELECT timestamp, value, junk, ... FROM

        can be used to initialize a TimeSeries instance. TimeSeries should therefore only
        take the first two attributes for data initialization, regardless of their names.
        """
        cur = self._db.cursor().execute('SELECT COUNT(*) from TestTable')
        nbrOfTuples = cur.fetchall()[0][0]
        cur = self._db.cursor().execute('SELECT timestamp, value, junk_one, junk_two FROM TestTable')
        ts = TimeSeries()
        ts.initialize_from_sql_cursor(cur)
        assert len(ts) == nbrOfTuples

    def select_star_test(self):
        """SELECT * FROM TestTable

        This function tests if statements like 

        SELECT * FROM

        can be used to initialize a TimeSeries instance. TimeSeries should therefore only
        take the first two attributes for data initialization, regardless of their names.
        """
        cur = self._db.cursor().execute('SELECT COUNT(*) from TestTable')
        nbrOfTuples = cur.fetchall()[0][0]
        cur = self._db.cursor().execute('SELECT * FROM TestTable')
        ts = TimeSeries()
        ts.initialize_from_sql_cursor(cur)
        assert len(ts) == nbrOfTuples

    def multidimensionaltimeseries_test(self):
        """Test the initialization of the MultiDimensionalTimeSeries."""
        cur = self._db.cursor().execute('SELECT COUNT(*) from TestTable')
        nbrOfTuples = cur.fetchall()[0][0]
        cur = self._db.cursor().execute('SELECT timestamp, value, junk_one FROM TestTable')
        ts = MultiDimensionalTimeSeries(dimensions=2)
        ts.initialize_from_sql_cursor(cur)
        assert len(ts) == nbrOfTuples

    def check_for_consistency_test(self):
        """Tests if database initialization and manual initialization create equal TimeSeries instances."""
        cur = self._db.cursor().execute('SELECT COUNT(*) from TestTable')
        nbrOfTuples = cur.fetchall()[0][0]
        sqlstmt = 'SELECT timestamp, value FROM TestTable ORDER BY timestamp ASC'
        tsManual = TimeSeries()
        data = self._db.cursor().execute(sqlstmt).fetchall()
        for entry in data:
            tsManual.add_entry(str(entry[0]), entry[1])

        tsAuto = TimeSeries()
        tsAuto.initialize_from_sql_cursor(self._db.cursor().execute(sqlstmt))
        assert nbrOfTuples == len(tsManual)
        assert nbrOfTuples == len(tsAuto)
        assert len(tsManual) == len(tsAuto)
        assert tsManual == tsAuto