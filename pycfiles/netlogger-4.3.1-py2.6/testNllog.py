# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testNllog.py
# Compiled at: 2010-09-28 19:46:09
"""
Unittests for nllog.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testNllog.py 26526 2010-09-28 23:46:08Z dang $'
import logging, optparse, os, re, sys
from tempfile import mkdtemp
import unittest
from netlogger.tests import shared
from netlogger import nllog

class Target:

    def __init__(self):
        self.clear()

    def handle(self, record):
        self.records.append(record.getMessage())

    def clear(self):
        self.records = []

    def flush(self):
        self.clear()


class TestCase(shared.BaseTestCase):

    def setUp(self):
        self._target1 = Target()
        self._target2 = Target()

    def _log_events(self):
        self.test_log.error('error', foo='bar')
        self.test_log.info('my.event', value=88.7, units='seconds')
        self.test_log.debug('debug')
        self.test_log.trace('trace')
        try:
            x = 1 / 0
        except Exception, err:
            self.test_log.exception('divbyzero', err, varname='x')

    def testBPLogger(self):
        """Basic BPLogger output.
        """
        nllog.set_logger_class(nllog.BPLogger)
        nllog.PROJECT_NAMESPACE = 'testBPLogger'
        g = nllog.get_root_logger()
        h = logging.handlers.MemoryHandler(1000)
        h.setTarget(self._target1)
        g.addHandler(h)
        g.setLevel(logging.INFO)
        self._target1.clear()
        self.records = {}
        input = [('test.start', 1), ('test.middle', 2), ('test.end', 3)]
        for (event, n) in input:
            g.info(event, n=n)

        h.flush()
        ns = nllog.PROJECT_NAMESPACE + '.'
        rec = self._target1.records
        for (i, (event, n)) in enumerate(input):
            m = re.search('event=(\\S+)', rec[i])
            self.assert_(m, "No 'event' in record '%s'" % (rec[i],))
            self.assert_(m.group(1) == ns + event, "Bad 'event' in record '%s': got %s, expected %s" % (
             rec[i], m.group(1), event))
            m = re.search('n=(\\S+)', rec[i])
            self.assert_(m, "No 'n' in record '%s'" % (rec[i],))
            self.assert_(int(m.group(1)) == n, "Bad 'n' in record '%s': got %s, expected %d" % (
             rec[i], m.group(1), n))

        g.removeHandler(h)

    def testBPSysLogger(self):
        """Basic BPSysLogger output, which includes an arbitrary header.
        """
        nllog.BPSysLogger.header = hdr = 'foo'
        nllog.set_logger_class(nllog.BPSysLogger)
        nllog.PROJECT_NAMESPACE = 'testBPSysLogger'
        g = nllog.get_root_logger()
        h = logging.handlers.MemoryHandler(1000)
        h.setTarget(self._target2)
        g.addHandler(h)
        g.setLevel(logging.INFO)
        self._target2.clear()
        self.records = {}
        input = [('test.start', 1), ('test.middle', 2), ('test.end', 3)]
        for (event, n) in input:
            g.info(event, n=n)

        h.flush()
        ns = nllog.PROJECT_NAMESPACE + '.'
        rec = self._target2.records
        for (i, (event, n)) in enumerate(input):
            m = re.search('%s: ts=' % hdr, rec[i])
            self.assert_(m, "No header '%s' in '%s'" % (hdr, rec[i]))
            m = re.search('event=(\\S+)', rec[i])
            self.assert_(m, "No 'event' in record '%s'" % (rec[i],))
            self.assert_(m.group(1) == ns + event, "Bad 'event' in record '%s': got %s, expected %s" % (
             rec[i], m.group(1), event))
            m = re.search('n=(\\S+)', rec[i])
            self.assert_(m, "No 'n' in record '%s'" % (rec[i],))
            self.assert_(int(m.group(1)) == n, "Bad 'n' in record '%s': got %s, expected %d" % (
             rec[i], m.group(1), n))

        g.removeHandler(h)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()