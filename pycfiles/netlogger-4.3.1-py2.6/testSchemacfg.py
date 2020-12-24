# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testSchemacfg.py
# Compiled at: 2010-10-15 14:38:49
"""
Unittests for netlogger.analysis.schemacfg
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testSchemacfg.py 26609 2010-10-15 18:38:47Z dang $'
import datetime, glob, logging, math, sys, time, unittest
from netlogger.tests import shared
from netlogger.analysis import schemacfg
from netlogger import nlapi
from netlogger import nldate
from netlogger import nllog
from netlogger.parsers import base

class TestCase(shared.BaseTestCase):
    """Unit test cases.
    """

    def setUp(self):
        self.basic_schema = '%s/%s' % (self.data_dir, 'basic_schema.cfg')
        self.formatter = nlapi.Log(level=nlapi.Level.ALL)
        self.parser = base.NLSimpleParser()
        log = nllog.get_logger('analysis.schemacfg')
        if self.DEBUG:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.WARN)
        log.addHandler(logging.StreamHandler(sys.stderr))

    def testBasic(self):
        """Test a basic schema.
        """
        parser = schemacfg.SchemaParser(files=(self.basic_schema,))
        schema = parser.get_schema()
        for i in range(3):
            event_attr = {'count': i, 'value': i * math.pi, 
               'msg': '%d times pi' % i, 
               'status': 0, 
               'date': '2010-09-29T12:34:56.001Z'}
            estr = self.formatter.info('basic', **event_attr)
            self.debug_("Event: '%s'" % estr.strip())
            e = self.parser.parseLine(estr)
            for (key, value) in event_attr.items():
                self.assert_(key in e, "Missing attribute: '%s'" % key)
                evalue = e[key]
                self.assert_(isinstance(evalue, str), '%s=%s is type %s, not str' % (
                 key, evalue, type(evalue)))

            schema.event(e)
            for (key, value) in event_attr.items():
                self.assert_(key in e, "Missing attribute: '%s'" % key)
                evalue = e[key]
                evalue_type = type(evalue)
                if key == 'date':
                    expect_type = datetime.datetime
                else:
                    expect_type = type(value)
                self.assert_(evalue_type == expect_type, '%s=%s is type %s, not type %s' % (
                 key, evalue, evalue_type, expect_type))

            input_date = datetime.datetime.utcfromtimestamp(nldate.parseISO(event_attr['date']))
            got_date = e['date']
            self.assertEqual(input_date, got_date)

        for i in range(3):
            event_attr = {'count': i}
            estr = self.formatter.info(('basic.%d' % i), **event_attr)
            self.debug_("Event: '%s'" % estr.strip())
            e = self.parser.parseLine(estr)
            for (key, value) in event_attr.items():
                self.assert_(key in e, 'Missing attribute %s' % key)
                evalue = e[key]
                self.assert_(isinstance(evalue, str), '%s=%s is type %s, not str' % (
                 key, evalue, type(evalue)))

            schema.event(e)
            for (key, value) in event_attr.items():
                self.assert_(key in e, 'Missing attribute %s' % key)
                evalue = e[key]
                self.assert_(isinstance(evalue, str), '%s=%s is type %s, not str' % (
                 key, evalue, type(evalue)))

    def testBadInput(self):
        """Give bad input and make sure it fails gracefully
        """
        parser = schemacfg.SchemaParser()
        for bogus_file in (None, '', '/bogus'):
            self.assertRaises(IOError, parser.read, bogus_file)
            schema = parser.get_schema()
            self.assertEqual(schema.mapping, {})

        for bogus_schema in glob.glob('%s/bogus_schema_*.cfg' % self.data_dir):
            self.assertRaises(ValueError, schemacfg.SchemaParser, (
             bogus_schema,))

        return


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()