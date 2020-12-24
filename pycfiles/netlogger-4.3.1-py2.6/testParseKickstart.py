# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/component/testParseKickstart.py
# Compiled at: 2009-12-08 17:43:28
"""
Unittests for kickstart.py
"""
__author__ = 'Keith Beattie KSBeattie@lbl.gov'
__rcsid__ = '$Id: testParseKickstart.py 23798 2009-07-14 17:18:22Z dang $'
import unittest
from netlogger.tests import shared
from netlogger.parsers.modules.kickstart import Parser

class TestCase(shared.BaseParserTestCase):
    """ TestCases for the kickstart parser. """
    QUICKSTART = ' <?xml version="1.0" encoding="ISO-8859-1"?>\n<invocation xmlns="http://pegasus.isi.edu/schema/invocation" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://pegasus.isi.edu/schema/invocation http://pegasus.isi.edu/schema/iv-2.0.xsd" version="2.0" start="2007-09-11T11:19:23.202-07:00" duration="0.923" transformation="mImgtbl:3.0" derivation="mImgtbl1:1.0" resource="isi_viz" hostaddr="128.9.72.170" hostname="viz-1.isi.edu" pid="11270" uid="1027" user="vahi" gid="1027" group="vahi" umask="0022">\n  <mainjob start="2007-09-11T11:19:23.206-07:00" duration="0.919" pid="11271">\n    <usage utime="0.107" stime="0.042" minflt="2419" majflt="0" nswap="0" nsignals="0" nvcsw="787" nivcsw="0"/>\n    <status raw="0"><regular exitcode="0"/></status>\n    <statcall error="0">\n      <!-- deferred flag: 0 -->\n      <file name="/nfs/software/montage/default/bin/mImgtbl">7F454C46010101000000000000000000</file>\n      <statinfo mode="0100755" size="1690959" inode="1042591" nlink="1" blksize="32768" blocks="3312" mtime="2007-05-29T14:18:58-07:00" atime="2007-09-11T07:14:50-07:00" ctime="2007-05-29T14:18:58-07:00" uid="0" user="root" gid="0" group="root"/>\n    </statcall>\n    <argument-vector>\n      <arg nr="1">.</arg>\n      <arg nr="2">-t</arg>\n      <arg nr="3">cimages_20070606_144238_27047.tbl</arg>\n      <arg nr="4">newcimages.tbl</arg>\n    </argument-vector>\n  </mainjob>\n  <cwd>/nfs/shared-scratch/vahi/exec/workdir/vahi/pegasus/montage-1.0/run0012</cwd>\n  <usage utime="0.002" stime="0.003" minflt="170" majflt="1" nswap="0" nsignals="0" nvcsw="81" nivcsw="1"/>\n  <uname system="linux" archmode="IA32" nodename="viz-1" release="2.6.11.7" machine="i686">#3 SMP Tue Nov 22 17:17:26 PST 2005</uname>\n  <statcall error="0" id="stdin">\n    <!-- deferred flag: 0 -->\n    <file name="/dev/null"/>\n    <statinfo mode="020666" size="0" inode="1899" nlink="1" blksize="4096" blocks="0" mtime="2007-03-07T17:28:03-08:00" atime="2007-03-07T17:28:03-08:00" ctime="2007-03-07T17:28:03-08:00" uid="0" user="root" gid="0" group="root"/>\n  </statcall>\n  <statcall error="0" id="stdout">\n    <temporary name="/tmp/gs.out.tNy5Vp" descriptor="3"/>\n    <statinfo mode="0100600" size="40" inode="174" nlink="1" blksize="4096" blocks="8" mtime="2007-09-11T11:19:24-07:00" atime="2007-09-11T11:19:23-07:00" ctime="2007-09-11T11:19:24-07:00" uid="1027" user="vahi" gid="1027" group="vahi"/>\n    <data>[struct stat=&quot;OK&quot;, count=49, badfits=0]\n</data>\n  </statcall>\n  <statcall error="0" id="stderr">\n    <temporary name="/tmp/gs.err.ibjOHF" descriptor="4"/>\n    <statinfo mode="0100600" size="0" inode="175" nlink="1" blksize="4096" blocks="0" mtime="2007-09-11T11:19:23-07:00" atime="2007-09-11T11:19:23-07:00" ctime="2007-09-11T11:19:23-07:00" uid="1027" user="vahi" gid="1027" group="vahi"/>\n  </statcall>\n  <statcall error="0" id="gridstart">\n    <!-- deferred flag: 0 -->\n    <file name="/nfs/home/vahi/PEGASUS/default/bin/kickstart">7F454C46010101000000000000000000</file>\n    <statinfo mode="0100755" size="133757" inode="2208186" nlink="1" blksize="32768" blocks="272" mtime="2007-09-11T12:14:51-07:00" atime="2007-09-11T12:07:09-07:00" ctime="2007-09-11T12:07:09-07:00" uid="1027" user="vahi" gid="1027" group="vahi"/>\n  </statcall>\n  <statcall error="0" id="logfile">\n    <descriptor number="1"/>\n    <statinfo mode="0100600" size="0" inode="342167" nlink="1" blksize="4096" blocks="0" mtime="2007-09-11T11:19:23-07:00" atime="2007-09-11T11:19:23-07:00" ctime="2007-09-11T11:19:23-07:00" uid="1027" user="vahi" gid="1027" group="vahi"/>\n  </statcall>\n  <statcall error="0" id="channel">\n    <fifo name="/tmp/gs.app.ZyZTqV" descriptor="5" count="0" rsize="0" wsize="0"/>\n    <statinfo mode="010640" size="0" inode="176" nlink="1" blksize="4096" blocks="0" mtime="2007-09-11T11:19:23-07:00" atime="2007-09-11T11:19:23-07:00" ctime="2007-09-11T11:19:23-07:00" uid="1027" user="vahi" gid="1027" group="vahi"/>\n  </statcall>\n</invocation>\n'
    basename = 'kickstart.'
    parser_class = Parser

    def testMultiEvent(self):
        """ Parse kickstart into multiple events. """
        self.setInput(self.QUICKSTART)
        parser = Parser(self.sio, raw=True)
        event = shared.getNextEvent(parser)
        self.debug_('parsed event: %s' % event)
        self.failUnless(event['event'].endswith('invocation.start'), "First event '%s' should be an invocation.start event" % event['event'])
        self.must_have(event, {'transformation': 'mImgtbl:3.0'})
        event = shared.getNextEvent(parser)
        self.debug_('parsed event: %s' % event)
        self.failUnless(event['event'].endswith('invocation.end'), "First event '%s' should be an invocation.end event" % event['event'])
        self.must_have(event, {'status': 0})
        self.assertRaises(StopIteration, shared.getNextEvent, parser)

    def testOneEvent(self):
        """ Parse kickstart into one event. """
        self.setInput(self.QUICKSTART)
        parser = Parser(self.sio, raw=True, one_event=True)
        event = shared.getNextEvent(parser)
        self.debug_('parsed event: %s' % event)
        self.failUnless(event['event'].endswith('invocation'), "First event '%s' should be an invocation event" % event['event'])
        self.must_have(event, {'transformation': 'mImgtbl:3.0', 'status': 0})
        self.assertRaises(StopIteration, shared.getNextEvent, parser)

    def testFailedStat(self):
        """Parse kickstart with failed 'statcall' in it.
        """

        def _test(event, num):
            data = ({'event': 'pegasus.invocation'},
             {'event': 'pegasus.invocation.stat.error', 'status': 100})[num]
            self.must_have(event, data)

        self.checkGood(filename='failed_stat', num_expected=2, test=_test, parser_kw=dict(one_event=True))

    def testEmptyStatinfo(self):
        """Parse kickstart with failed 'statcall' that has no statinfo"""
        self.checkGood(filename='empty_statinfo', num_expected=2, parser_kw=dict(one_event=True))


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()