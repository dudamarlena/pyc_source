# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testAnalyzeMongo.py
# Compiled at: 2010-08-16 16:59:58
"""
Unittests for analysis/modules/mongodb.py

If the import of mongodb fails, or the initial connect fails, this 
will just stop with an error.
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testAnalyzeMongo.py 25126 2010-08-16 20:59:57Z dang $'
import re, time
from pymongo.connection import Connection
from netlogger.tests import shared
import unittest
from netlogger.analysis.modules import mongodb

class TestCase(shared.BaseTestCase):
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    DBNAME = 'nl_test_db'
    COLLNAME = 'nl_test_collection'

    def setUp(self):
        shared.BaseTestCase.setUp(self)
        self._clearDB()

    def tearDown(self):
        pass

    def _clearDB(self):
        """Drop the database.
        """
        Connection(host=self.MONGO_HOST, port=self.MONGO_PORT).drop_database(self.DBNAME)

    def _create(self, **kw):
        """Create Analyzer instance.
        """
        a = mongodb.Analyzer(host=self.MONGO_HOST, port=self.MONGO_PORT, database=self.DBNAME, collection=self.COLLNAME, **kw)
        return a

    def _connect_to_db(self):
        """Connect to mongodb, return collection instance."""
        return Connection(host=self.MONGO_HOST, port=self.MONGO_PORT)[self.DBNAME]

    def _connect_to_collection(self):
        """Connect to mongodb, return collection instance."""
        return self._connect_to_db()[self.COLLNAME]

    def _event(self, count, name='test.event'):
        """Generate an event dictionary."""
        return {'ts': time.time(), 'count': count, 
           'event': name}

    def _check_all(self, events):
        """Check that exactly the events in the provided list
        are in the database.
        They do not necessarily have to be in the same order.
        """
        time.sleep(1)
        coll = self._connect_to_collection()
        makekey = lambda e: (e['event'], e['count'])
        saved_events = {}
        for e in coll.find():
            key = makekey(e)
            saved_events[key] = 1

        for e in events:
            key = makekey(e)
            self.failUnless(key in saved_events, '%s not found in db' % e)
            del saved_events[key]

        if saved_events:
            self.fail('%d extra events in db' % len(saved_events))

    def testDefaults(self):
        """Default options.
        """
        analyzer = self._create()
        events = []
        for i in xrange(100):
            e = self._event(i)
            analyzer.process(e)
            events.append(e)

        analyzer.finish()
        self._check_all(events)

    def testEventFilter(self):
        """Option 'event_filter'
        """
        events = []
        for (expr_num, expr) in enumerate(('half.*', '.*\\-pass', '.*alf')):
            analyzer = self._create(event_filter=expr)
            for i in xrange(100):
                e = self._event(i, 'half-pass-%d' % expr_num)
                analyzer.process(e)
                events.append(e)
                e2 = self._event(i)
                e2['event'] = 'ignore.me'
                analyzer.process(e2)

        analyzer.finish()
        for (expr_num, expr) in enumerate(('', '.*')):
            analyzer = self._create(event_filter=expr)
            for i in xrange(100):
                e = self._event(i, 'all-pass-%d' % expr_num)
                analyzer.process(e)
                events.append(e)

        analyzer.finish()
        for expr in ('foobar', '\\s\\w*', '^$'):
            analyzer = self._create(event_filter=expr)
            for i in xrange(100):
                e = self._event(i, 'no-pass')
                analyzer.process(e)

        analyzer.finish()
        self._check_all(events)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()