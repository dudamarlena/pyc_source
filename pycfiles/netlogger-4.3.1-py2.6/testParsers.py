# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testParsers.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for nvParser.py
"""
__author__ = 'Keith Jackson krjackson@lbl.gov'
__rcsid__ = '$Id: testParsers.py 23798 2009-07-14 17:18:22Z dang $'
import os
from StringIO import StringIO
import sys
from tempfile import TemporaryFile
import unittest
from netlogger import nlapi
from netlogger.parsers.base import NLFastParser, NLPyParser, parseDate
from netlogger.parsers.base import BaseParser
from netlogger.parsers.modules import bp, generic
from netlogger.tests import shared
log_events = (
 (' ts=2007-08-16T13:11:42.643255Z id=10270 event=e1 u=host:30003/', ''),
 ('ts=2007-08-16T13:12:20.648918-08:00 id=1 event=e2 foo=" bA a r"', ''),
 ('ts=2007-08-16T13:17:31.824379Z id=foo', 'no event'),
 ('ts=2007-08-16T13:18:02.404602Z id=this is not right at all', 'format'),
 ('ts=2007-08-16T13:18:02.477603Z id=10324 event="e 3" session_id=22', ''),
 ('ts=2007-08-16T13:18:02.575615+99 event=e4 session_id=2 status=0', 'ts'),
 ('id=10324 event=e5 ts=2007-08-16T13:18:02.576034+01:30', ''))
test_log = ('\n').join([ e[0] for e in log_events ]) + '\n'
err_events = filter(lambda e: e[1] != '', log_events)
num_ok = {'total': len(log_events) - len(err_events), 
   'beforeError': min([ (99, i)[bool(e[1])] for (i, e) in enumerate(log_events) ])}

class TestCase(shared.BaseParserTestCase):

    def setUp(self):
        shared.BaseParserTestCase.setUp(self)
        self.had_err = []
        nlapi.clearGuid()

    def dummy(self, line=None, error=None, linenum=0):
        self.debug_('parse error on line %d', linenum)
        self.had_err.append((linenum, str(error)))

    def testParseStream(self):
        """Parse a stream with pyparsing.
         """
        self.debug_('NLPyParsing')
        sio = StringIO(test_log)
        try:
            parser = NLPyParser(sio, err_cb=self.dummy)
        except NotImplementedError:
            self.debug_('pyparsing is not installed, skipping test')
            return
        else:
            for x in parser.parseStream():
                pass

            self.debug_('error list: %s' % self.had_err)
            for (i, e) in self.had_err:
                self.failUnless(log_events[i][1] != '', "unexpected failure on '%s': %s" % (
                 log_events[i][0], e))

            for (i, (msg, is_err)) in enumerate(log_events):
                if not is_err:
                    continue
                j = -1
                for (j, _) in self.had_err:
                    if i == j:
                        break

                if i != j:
                    self.failUnless(i == j, "undetected bad event '%s'" % msg)

    def testParseFastStream(self):
        """Parse with the regex-based parser.
        """
        errfn_ok = {None: num_ok['beforeError'], False: num_ok['total'], 
           self.dummy: num_ok['total']}
        self.debug_('parse fast stream:\n%s' % test_log)
        for errfn in errfn_ok.keys():
            self.debug_('error fn=%s' % errfn)
            sio = StringIO(test_log)
            parser = NLFastParser(sio, err_cb=errfn, verify=True)
            try:
                i = 0
                genfn = parser.parseStream()
                for d in genfn:
                    i += 1

            except ValueError, E:
                pass

            expected = errfn_ok[errfn]
            self.failUnless(i == expected, 'with err callback (%s): expected %d items, got %d' % (
             errfn, expected, i))

        return

    def testParseDate(self):
        """Test correctness of date parsing with and without timezones.
        """
        dates = {'1970-01-01T00:00:00Z': 0, 
           '1969-12-31T16:00:01-08:00': 1, 
           '2009-02-13T15:31:30.987654-08:00': 1234567890.987654, 
           '2009-02-13T23:31:30.987654Z': 1234567890.987654, 
           '2009-02-13T23:31:30.000000001Z': 1234567890.0, 
           '1234567890.000000001': 1234567890.0}
        for (iso, expected_sec) in dates.items():
            sec = parseDate(iso)
            self.failUnless(sec == expected_sec, "date '%s' returned %lfs, but expected %lfs" % (
             iso, sec, expected_sec))

        dates = ('', ' ', 'foo', '-foo', '2009-02-13T15:31:30.987654-08:00Z', '2009-02-13T15:31:30-0800',
                 '2009-02-13T15:31:30-08:0')
        for bad_date in dates:
            try:
                sec = parseDate(bad_date)
                self.fail("bad date '%s' parsed as %lf seconds" % (
                 bad_date, sec))
            except ValueError:
                pass

        soso_dates = ('2009-02-13T15:31:30.987654', '2009-02-13T15:31:30')
        for soso in soso_dates:
            parseDate(soso)

        import time
        (N, iso) = (10000, '2009-02-13T15:31:30.987654-08:00')
        t = time.time()
        for i in xrange(N):
            sec = parseDate(iso)

        usec = (time.time() - t) / N * 1000000.0
        self.debug_("avg time to parse '%s' = %.1lf us" % (iso, usec))

    class OneCharParser(BaseParser):
        """Split input line into multiple events, 1 per char.
        """

        def process(self, line):
            result = []
            for chr in line.strip():
                result.append({'ts': 0, 'event': 'x', 'chr': chr})

            return result

    def testMultipleEventsPerLine(self):
        """Test correctness of file offset mid-resultset.
        """
        tmpf = TemporaryFile()
        data = ('abcd*', 'fghi*')
        tmpf.write(('\n').join(data) + '\n')
        tmpf.seek(0)
        parser = self.OneCharParser(tmpf)
        offset = 0
        for line in data:
            for c in line:
                e = parser.next()
                chr = e['chr']
                self.failUnless(chr == c, "wrong character: wanted '%s' got '%s'" % (
                 c, chr))
                self.failUnless(parser.getOffset() == offset, 'wrong offset')
                if c == '*':
                    offset += len(line) + 1

    def testBPParser(self):
        """Best-Practices  parser, including extra params"""
        iso_time = '2009-07-11T08:31:45.123Z'
        sec_time = 1247301105.123
        template = 'ts=%s event=foo level=Info n=%%d\n' % iso_time
        input = []
        for i in xrange(10):
            input.append(template % i)

        sio = StringIO(('').join(input))
        p = bp.Parser(sio, parse_date=True)
        for (i, event) in enumerate(p):
            ts = event['ts']
            self.assert_(ts == sec_time, 'Expected ts=%lf got ts=%lf' % (
             sec_time, ts))

        sio = StringIO(('').join(input))
        p = bp.Parser(sio, parse_date=False)
        for (i, event) in enumerate(p):
            ts = event['ts']
            self.assert_(ts == iso_time, 'Expected ts=%s got ts=%s' % (
             iso_time, ts))

        kw = {'hello': 'world', 'howya': 'doin'}
        sio = StringIO(('').join(input))
        p = bp.Parser(sio, **kw)
        for (i, event) in enumerate(p):
            for (name, value) in kw.items():
                self.assert_(event.has_key(name), "event %s is missing keyword '%s'" % (
                 event, name))
                self.assert_(event[name] == kw[name], 'event value %s differs from input %s for keyword %s' % (
                 event[name], kw[name],
                 name))

    def testOffset(self):
        """File offset is calculated correctly even with 'bad' events.
        """
        from netlogger.parsers.modules import sge_rpt
        self.parser_class = sge_rpt.Parser
        self.basename = 'sge_rpt.'
        parser = self.checkGood('some-not-parseable', test=lambda e: True)
        file_length = os.stat(parser._infile.name)[6]
        self.assert_(file_length > 0, 'input file %s is empty' % parser._infile.name)
        offs = parser.getOffset()
        self.assert_(file_length == offs, 'file length %d != offset %d' % (
         file_length, offs))


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()