# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/system/testNlParse.py
# Compiled at: 2010-09-16 18:50:23
"""
Test some interesting bits of nl_parse
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: testNlParse.py 25215 2010-09-16 22:50:21Z dang $'
import os, re, signal
from subprocess import Popen, STDOUT
import tempfile, time
from netlogger.tests import shared
from netlogger import nlapi
from netlogger.nldate import utcFormatISO
EVENT1 = 'ts=2008-04-22T23:15:10.266296Z event=test'

class TestCase(shared.BaseTestCase):

    def setUp(self):
        self._filename = None
        self._clear_logdir()
        return

    def tearDown(self):
        if self._filename:
            os.unlink(self._filename)
        if not self.DEBUG:
            self._clear_logdir()

    def _clear_logdir(self):
        d = self.get_temp_logdir()
        if os.path.exists(d):
            for f in os.listdir(d):
                self.debug_('removing %s/%s' % (d, f))
                os.unlink('%s/%s' % (d, f))

        else:
            os.mkdir(d)

    def get_temp(self):
        return '/tmp/system.testNlParse.%d' % os.getpid()

    def get_temp_logdir(self):
        return '/tmp/system.testNlParse.logs'

    def testNlParseBlocking(self):
        """Whether nl_parse properly times out in 'tail' mode when
        the input source remains open but sends no data, as could occur
        in a socket or UNIX pipe.
        """
        self.program = 'nl_parse'
        (flush_time, n) = (1, 10)
        my_tempfile = open(self.get_temp(), 'w')
        self._filename = my_tempfile.name
        my_tempfile.close()
        args = ['-t', '-F%d' % flush_time, '-f', self._filename, 'bp']
        proc = self.cmd(args, 'fork', pipe_stdin=True)
        self.assert_(proc, 'No process forked')
        self.assert_(proc.poll() is None, 'Process died')
        time.sleep(1)
        for i in xrange(n):
            proc.stdin.write(EVENT1 + ' i=%d \n' % i)

        proc.stdin.close()
        for wait_count in xrange(flush_time + 1):
            time.sleep(1)

        n_lines = self.get_result()
        self.failUnless(n_lines == n, 'Num. lines in file (%d) != number written (%d)' % (
         n_lines, n))
        return

    def testNlParseRollover(self):
        """Following rolled-over (truncated) files.
        """
        prog = shared.script_path('nl_parse')
        pause = 0.5
        offs_temp = self.get_temp() + '.offset'
        logdir = self.get_temp_logdir()
        output_file = '%s/parser.out' % logdir
        devnull = open('/dev/null', 'w')
        for offs_option in (None, offs_temp):
            for verbose_option in (None, '-v', '-vv'):
                scan = 1
                (N, N2) = (5, 3)
                args = [
                 prog]
                if offs_option:
                    args.extend(['-O', offs_option])
                if verbose_option:
                    args.append(verbose_option)
                args.extend(['-t', '-s', str(scan), '-o', output_file,
                 'bp', '%s/*.log' % logdir])
                self.debug_('Run: %s' % str(args))
                if self.DEBUG:
                    proc = Popen(args)
                else:
                    proc = Popen(args, stdout=devnull.fileno(), stderr=STDOUT)
                self.assert_(proc, 'No process forked')
                self.assert_(proc.poll() is None, 'Process died')
                time.sleep(pause)
                log_files = [ '%s/%s.log' % (logdir, name) for name in ('a', 'b', 'c')
                            ]
                logs = [ nlapi.Log(log_file, guid=False, flush=True, meta={'file': log_file}) for log_file in log_files
                       ]
                self.debug_('Write logs #1')
                for i in xrange(N):
                    for g in logs:
                        g.info('before-roll', iteration=i)

                time.sleep(scan + pause)
                del logs
                self.debug_('Roll')
                for log_file in log_files:
                    os.rename(log_file, log_file + '.rolled')

                logs = [ nlapi.Log(log_file, guid=False, meta={'file': log_file}, flush=True) for log_file in log_files
                       ]
                self.debug_('Write logs #2')
                for i in xrange(N2):
                    for g in logs:
                        g.info('after-roll', iteration=i)

                self.debug_('Wait for scan')
                time.sleep(scan + pause)
                self.debug_('Kill nl_parse')
                proc.kill()
                log_counts = dict.fromkeys(log_files, 0)
                self.debug_("Checking output in '%s'" % output_file)
                for line in open(output_file):
                    s = line.strip()
                    m = re.search('file=(\\S+)', s)
                    self.assert_(m, "bad log line '%s'" % s)
                    logfile = m.group(1)
                    log_counts[logfile] += 1

                for (key, value) in log_counts.items():
                    self.assert_(value == N + N2, "Output from '%s' had %d records, expected %d" % (
                     key, value, N + N2))

                self._clear_logdir()

        return

    def get_result(self):
        count = 0
        for line in file(self._filename, 'r'):
            count += 1

        return count


def suite():
    return shared.suite(TestCase)


if __name__ == '__main__':
    shared.main()