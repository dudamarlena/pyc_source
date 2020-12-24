# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/system/testScripts.py
# Compiled at: 2010-10-22 19:56:32
"""
Test basic, common functionality from each of the scripts,
e.g. that it has at least a working -h option.
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testScripts.py 26646 2010-10-19 23:45:40Z taghrid $'
import re
from subprocess import Popen, PIPE
import tempfile
from netlogger.tests import shared
sample_log = '\n2008/04/22 16:15:10 DEBUG> Request.pm:75 perfSONAR_PS::Request::parse - ts=2008-04-22T23:15:10.266296Z event=org.perfSONAR.Services.MA.clientRequest.start guid=e47c1ec9-10c1-11dd-9586-000f1f6fc256\n2008/04/22 16:15:13 DEBUG> SNMP.pm:734 perfSONAR_PS::Services::MA::SNMP::handleEvent - ts=2008-04-22T23:15:13.146751Z event=org.perfSONAR.Services.MA.handleEvent.end guid=e47c1ec9-10c1-11dd-9586-000f1f6fc256\n2008/04/22 16:15:13 DEBUG> Request.pm:248 perfSONAR_PS::Request::finish - ts=2008-04-22T23:15:13.286661Z event=org.perfSONAR.Services.MA.clientRequest.end guid=e47c1ec9-10c1-11dd-9586-000f1f6fc256\n\n'
sample_log2 = ' ts=2008-04-22T23:15:10.266296Z event=org.perfSONAR.Services.MA.clientRequest.start guid=e47c1ec9-10c1-11dd-9586-000f1f6fc256\n ts=2008-04-22T23:15:13.286661Z event=org.perfSONAR.Services.MA.clientRequest.end guid=e47c1ec9-10c1-11dd-9586-000f1f6fc256\n'

class TestCase(shared.BaseTestCase):
    scripts = [
     'nl_check', 'nl_cpuprobe',
     'nl_date', 'nl_findbottleneck', 'nl_findmissing',
     'nl_ganglia', 'nl_interval',
     'nl_view', 'nl_wflowgen', 'nl_write',
     'nl_load', 'nl_parse']

    def makeLog(self, log):
        f = tempfile.NamedTemporaryFile()
        f.write(log)
        return f

    def testHelp(self):
        """Test -h/--help for each script.
        """
        for script in self.scripts:
            self.program = script
            self.debug_('\nscript: %s' % self.program)
            self.cmd(['-h'], 'wait')
            self.cmd(['--help'], 'wait')

    def testNLView(self):
        """Test nl_view on some input.
        """
        self.program = 'nl_view'
        f = self.makeLog(sample_log)
        self.cmd(['-diIgmt', '--namespace=org.perfSONAR.', f.name], 'wait')

    def testNLNotify(self):
        """nl_notify
        """
        self.program = 'nl_notify'
        from_user = 'user@otherhost.org'
        to_user = 'user@somehost.com'
        prog = 'false'
        args = ['--from', from_user, '--to', to_user, '--test', prog]
        self.debug_('Args=%s' % args)
        output = Popen([self.program] + args, stdout=PIPE).communicate()[0]
        s = output.split('\n')
        self.debug_('notify output: %s' % s)
        self.assert_(re.match('To:.*%s' % to_user, s[1]))
        self.assert_(re.match('From:.*%s' % from_user, s[2]))
        self.assert_(re.match('Subject:.*Error.*%s' % prog, s[3]))

    def testNLCheck(self):
        """nl_check
        """
        self.program = 'nl_check'
        self.cmd(['-h'], action='wait')
        self.cmd([''], action='wait', should_fail=True)
        self.cmd(['/no/such/file/xxxxxxxxxxxx'], action='wait', should_fail=True)


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()