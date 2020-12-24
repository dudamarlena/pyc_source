# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testParseGatekeeper.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for parse_gatekeeper.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testParseGatekeeper.py 23635 2009-04-03 13:48:55Z dang $'
import sys, unittest
from netlogger import nldate
from netlogger.parsers.modules.gk import Parser
from netlogger.tests import shared

class TestCase(shared.BaseTestCase, shared.ParserTestCase):
    PID = 6577

    def setUp(self):
        self.setParser(Parser)

    def normalizeTimestamps(self, values, event):
        """Normalize timestamps to floats"""
        if not isinstance(values['date'], float):
            values['ts'] = nldate.guess(values['date'])[1]
        if not isinstance(event['ts'], float):
            event['ts'] = nldate.guess(event['ts'])[1]
        del values['date']

    def checkValues(self, values, data):
        self.normalizeTimestamps(values, data)
        self.debug_('Check input values %s <=> %s event' % (values, data))
        for (key, value) in values.items():
            key = key.replace('__', '.')
            self.assert_(data.has_key(key), "Missing value for '%s'" % key)
            self.assert_(data[key] == value, "For '%s': got '%s', wanted '%s'" % (key, data[key],
             value))

    def testJM(self):
        """Parse line starting with GATEKEEPER_JM_ID"""
        v = dict(process__id=self.PID, jm__id='0000006577.0000000000', date='2006-11-09.00:06:28', DN='DC=org/DC=doegrids/OU=People/CN=Nom De Plume 123456', host='128.105.121.51')
        result = self.parser.process('PID: %(process__id)d -- Notice: 0: GATEKEEPER_JM_ID %(date)s.%(jm__id)s for %(DN)s on %(host)s' % v)
        self.assertEqual(len(result), 1)
        e = result[0]
        v['date'] = v['date'].replace('.', 'T')
        self.checkValues(v, e)

    def testStart(self):
        """Parse line with 'starting at'"""
        v = dict(process__id=self.PID, date='Wed Mar 18 20:21:00 2009')
        result = self.parser.process('PID: %(process__id)d -- Notice: 6: /opt/osg-itb-0.92/globus/sbin/globus-gatekeeper pid=%(process__id)d starting at %(date)s' % v)
        self.assertEqual(len(result), 1)
        v['date'] = nldate.parseSyslogDate(v['date'])
        self.checkValues(v, result[0])

    def testConn(self):
        """Parse line with 'Got connection'"""
        v = dict(process__id=self.PID, host='131.243.2.11', date='Wed Mar 18 20:21:00 2009')
        result = self.parser.process('PID: %(process__id)d -- Notice: 6: Got connection %(host)s at %(date)s' % v)
        self.assertEqual(len(result), 1)
        v['date'] = nldate.parseSyslogDate(v['date'])
        self.checkValues(v, result[0])

    def testAuth(self):
        """Parse line starting with 'Authenticated', after a TIME"""
        v = dict(process__id=self.PID, DN='DC=org/DC=doegrids/OU=People/CN=Nom De Plume 123456', date='Wed Mar 18 20:23:00 2009')
        s = ('\n').join(('TIME: %(date)s' % v,
         ' PID: %(process__id)d -- Notice: 5: Authenticated globus user: %(DN)s' % v))
        result = self.feedRecord(s)
        self.assertEqual(len(result), 1)
        v['date'] = nldate.parseSyslogDate(v['date'])
        self.checkValues(v, result[0])

    def testEnd(self):
        """Parse line with 'Child ... started', which is the .end event"""
        v = dict(process__id=self.PID, child__process__id=self.PID + 101, date='Wed Mar 18 20:23:00 2009', status=0)
        s = ('\n').join(('TIME: %(date)s' % v,
         ' PID: %(process__id)d -- Notice: 0: Child %(child__process__id)d started' % v))
        result = self.feedRecord(s)
        self.assertEqual(len(result), 1)
        v['date'] = nldate.parseSyslogDate(v['date'])
        self.checkValues(v, result[0])

    def testFail(self):
        """Parse line starting with 'Failure:'"""
        v = dict(process__id=self.PID, date='Wed Mar 18 20:23:00 2009', status=-1, msg='GSS failed Major:01090000 Minor:00000000 Token:00000003')
        s = ('\n').join(('TIME: %(date)s' % v,
         ' PID: %(process__id)d -- Failure: %(msg)s' % v))
        result = self.feedRecord(s)
        self.assertEqual(len(result), 1)
        v['date'] = nldate.parseSyslogDate(v['date'])
        self.checkValues(v, result[0])


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()