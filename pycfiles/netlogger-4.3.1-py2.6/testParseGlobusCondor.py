# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/testParseGlobusCondor.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for parsers/modules/globus_condor.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testParseGlobusCondor.py 23653 2009-04-15 17:46:25Z dang $'
from StringIO import StringIO
import unittest
from netlogger.parsers.modules.globus_condor import Parser
from netlogger.tests import shared
SUBMIT_EVENT = '<c>\n    <a n="MyType"><s>SubmitEvent</s></a>\n    <a n="EventTypeNumber"><i>0</i></a>\n    <a n="MyType"><s>SubmitEvent</s></a>\n    <a n="EventTime"><s>2008-02-06T16:14:24</s></a>\n    <a n="Cluster"><i>2</i></a>\n    <a n="Proc"><i>0</i></a>\n    <a n="Subproc"><i>0</i></a>\n    <a n="SubmitHost"><s>&lt;131.243.2.182:40152&gt;</s></a>\n</c>'
EXEC_EVENT = '<c>\n    <a n="MyType"><s>ExecuteEvent</s></a>\n    <a n="EventTypeNumber"><i>1</i></a>\n    <a n="MyType"><s>ExecuteEvent</s></a>\n    <a n="EventTime"><s>2008-02-06T16:14:27</s></a>\n    <a n="Cluster"><i>2</i></a>\n    <a n="Proc"><i>0</i></a>\n    <a n="Subproc"><i>0</i></a>\n    <a n="ExecuteHost"><s>&lt;131.243.2.130:47659&gt;</s></a>\n</c>'
TERM_EVENT = '<c>\n    <a n="MyType"><s>JobTerminatedEvent</s></a>\n    <a n="EventTypeNumber"><i>5</i></a>\n    <a n="MyType"><s>JobTerminatedEvent</s></a>\n    <a n="EventTime"><s>2008-02-06T16:14:27</s></a>\n    <a n="Cluster"><i>2</i></a>\n    <a n="Proc"><i>0</i></a>\n    <a n="Subproc"><i>0</i></a>\n    <a n="TerminatedNormally"><b v="t"/></a>\n    <a n="ReturnValue"><i>0</i></a>\n    <a n="RunLocalUsage"><s>Usr 0 00:00:00, Sys 0 00:00:00</s></a>\n    <a n="RunRemoteUsage"><s>Usr 0 00:00:00, Sys 0 00:00:00</s></a>\n    <a n="TotalLocalUsage"><s>Usr 0 00:00:00, Sys 0 00:00:00</s></a>\n    <a n="TotalRemoteUsage"><s>Usr 0 00:00:00, Sys 0 00:00:00</s></a>\n    <a n="SentBytes"><r>0.000000000000000E+00</r></a>\n    <a n="ReceivedBytes"><r>0.000000000000000E+00</r></a>\n    <a n="TotalSentBytes"><r>0.000000000000000E+00</r></a>\n    <a n="TotalReceivedBytes"><r>0.000000000000000E+00</r></a>\n</c>'
PREMATURE = '<c>\n    <a n="MyType"><s>SubmitEvent</s></a>\n<c>'
NOPROC = '<c>\n    <a n="MyType"><s>SubmitEvent</s></a>\n    <a n="EventTypeNumber"><i>0</i></a>\n    <a n="MyType"><s>SubmitEvent</s></a>\n    <a n="EventTime"><s>2008-02-06T16:14:24</s></a>\n    <a n="SubmitHost"><s>&lt;131.243.2.182:40152&gt;</s></a>'
NOTS = '<c>\n    <a n="MyType"><s>ExecuteEvent</s></a>\n    <a n="EventTypeNumber"><i>1</i></a>\n    <a n="MyType"><s>ExecuteEvent</s></a>\n    <a n="Cluster"><i>2</i></a>\n    <a n="Proc"><i>0</i></a>\n    <a n="Subproc"><i>0</i></a>\n    <a n="ExecuteHost"><s>&lt;131.243.2.130:47659&gt;</s></a>\n</c>'

class TestCase(shared.BaseTestCase, shared.ParserTestCase):
    """Unit test cases.
    """

    def setUp(self):
        """Setup actions
        """
        self.setParser(Parser)

    def tearDown(self):
        """Any cleanup actions
        """
        pass

    def verifyResult(self, result, expected):
        n = len(result)
        self.failUnless(n == expected, 'returned %d results instead of %d' % (n, expected))

    def testSubmitSimple(self):
        """Parse SubmitEvent and check that it returns a single result
        """
        self.debug_('Input:\n%s' % SUBMIT_EVENT)
        result = self.feedRecord(SUBMIT_EVENT)
        self.verifyResult(result, 1)

    def testExecSimple(self):
        """Parse ExecuteEvent and check that it returns a single result
        """
        result = self.feedRecord(EXEC_EVENT)
        self.verifyResult(result, 1)

    def testTermSimple(self):
        """Parse JobTerminatedEvent and check that it returns a single result
        """
        result = self.feedRecord(TERM_EVENT)
        self.verifyResult(result, 1)

    def testPremature(self):
        """Premature new record should abort old one"""
        self.assertRaises(ValueError, self.feedRecord, PREMATURE)
        result = self.feedRecord(SUBMIT_EVENT[4:])
        self.verifyResult(result, 1)

    def testMissingClusterProcOrSubproc(self):
        """If any one of cluster, proc, or subproc is missing, should raise a KeyError"""
        for add_fields in ('Cluster', ('Cluster', 'Proc'), ('Cluster', 'Subproc'),
         'Proc', 'Subproc', ('Proc', 'Subproc')):
            bad_event = NOPROC
            for field in add_fields:
                formatted_field = '\n<a n="%s"><i>0</i></a>' % field
                bad_event += formatted_field

            bad_event += '\n</c>'
            self.assertRaises(KeyError, self.feedRecord, bad_event)

        result = self.feedRecord(SUBMIT_EVENT)
        self.verifyResult(result, 1)

    def testMissingTimestamp(self):
        """If timestamp is missing, should raise a ValueError"""
        self.assertRaises(KeyError, self.feedRecord, NOTS)
        result = self.feedRecord(SUBMIT_EVENT)
        self.verifyResult(result, 1)

    def testBlank(self):
        """Blank line should do nothing"""
        result = self.parser.process('')
        self.verifyResult(result, 0)

    def testNonXML(self):
        """Non-xml lines (garbage) should raise ValueError-s"""
        for line in ('A common mistake that people make', 'when trying to design something completely foolproof',
                     'is to underestimate the ingenuity of complete fools.'):
            self.assertRaises(ValueError, self.feedRecord, line)

    def testJobID(self):
        """Job id should be composed from cluster, proc and subproc"""
        result = self.feedRecord(SUBMIT_EVENT)
        self.verifyResult(result, 1)
        jobid = result[0]['job.id']
        expected = '002.000.000'
        self.failUnless(jobid == expected, "Found job.id '%s' != '%s' expected" % (
         jobid, expected))

    def testEventName1(self):
        """Submit event name should be in NetLogger-style in namespace globus.condor"""
        result = self.feedRecord(SUBMIT_EVENT)
        self.verifyResult(result, 1)
        expected = 'globus.condor.submit'
        found = result[0]['event']
        self.failUnless(expected == found, "Found event name '%s' != '%s' expected" % (
         found, expected))

    def testEventName2(self):
        """Terminated event name should be in NetLogger-style in namespace globus.condor"""
        result = self.feedRecord(TERM_EVENT)
        self.verifyResult(result, 1)
        expected = 'globus.condor.jobTerminated'
        found = result[0]['event']
        self.failUnless(expected == found, "Found event name '%s' != '%s' expected" % (
         found, expected))


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()