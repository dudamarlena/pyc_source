# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testParseGridftpAuth.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for parse_gridftp_auth.py
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testParseGridftpAuth.py 23798 2009-07-14 17:18:22Z dang $'
from netlogger.tests import shared
import unittest
from netlogger.parsers.modules import gridftp_auth

class TestCase(shared.BaseParserTestCase):
    basename = 'gridftp-auth.'
    parser_class = gridftp_auth.Parser

    def testBasic(self):
        """parse an error-free gridftp_auth log
        """
        self.checkGood('basic', self._verifyBasic, num_expected=8)

    def _verifyBasic(self, e, num):
        name = e['event']
        if name == gridftp_auth.ns('conn.start'):
            self.assert_(e['host'] == 'some.host.org')
            self.assert_(e['port'] == 8888)

    def testErrors(self):
        """parse an error-laden gridftp_auth log
        """
        self.checkGood('errors', self._verifyErrors, num_expected=23, parser_kw={'error_timeout': '1 hour'})

    def _verifyErrors(self, e, num):
        name = e['event']
        if num == 12 or num == 15:
            self.assert_(name.endswith('.error'))
        else:
            self.failIf(name.endswith('.error'))

    def testSyslogBasic(self):
        """parse an error-free gridftp_auth log with a syslog header"""
        self.setParseDynamic(True, pattern='(?P<host>[a-zA-Z0-9.]+) ', show_header_groups=True)
        self.checkGood('syslog-basic', self._verifySyslog, num_expected=8)
        self.setParseDynamic(False)

    def _verifySyslog(self, e, num):
        self.assert_(e.has_key('syslog.host'))

    def testSyslogErrors(self):
        """parse an error-laden gridftp_auth log with a syslog header"""
        self.setParseDynamic(True, pattern='(?P<host>[a-zA-Z0-9.]+) ', show_header_groups=True)
        self.checkGood('syslog-error', self._verifySyslogErrors, num_expected=4)
        self.setParseDynamic(False)

    def _verifySyslogErrors(self, e, num):
        self.assert_(e.has_key('syslog.host'))
        host = e['syslog.host']
        name = e['event']
        events = [ gridftp_auth.ns(x) for x in ('conn.transfer.start', 'conn.transfer.end',
                                                'conn.transfer.start', 'conn.transfer.error')
                 ]
        self.assert_(name == events[num], "event name %d, '%s' not '%s'" % (
         num, name, events[num]))
        hosts = ['myhost.mydomain.org'] * 4
        hosts[2] = 'myhost2.mydomain.org'
        self.assert_(host == hosts[num], "host %d, '%s' not '%s'" % (
         num, host, hosts[num]))


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()