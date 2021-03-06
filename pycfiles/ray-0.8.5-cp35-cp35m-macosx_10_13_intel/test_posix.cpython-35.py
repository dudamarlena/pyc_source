# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/nz/vv4_9tw56nv9k3tkvyszvwg80000gn/T/pip-unpacked-wheel-c6tqtva7/psutil/tests/test_posix.py
# Compiled at: 2020-05-06 17:45:43
# Size of source mod 2**32: 16537 bytes
"""POSIX specific tests."""
import datetime, errno, os, re, subprocess, time, psutil
from psutil import AIX
from psutil import BSD
from psutil import LINUX
from psutil import MACOS
from psutil import OPENBSD
from psutil import POSIX
from psutil import SUNOS
from psutil.tests import CI_TESTING
from psutil.tests import get_kernel_version
from psutil.tests import get_test_subprocess
from psutil.tests import HAS_NET_IO_COUNTERS
from psutil.tests import mock
from psutil.tests import PYTHON_EXE
from psutil.tests import reap_children
from psutil.tests import retry_on_failure
from psutil.tests import sh
from psutil.tests import skip_on_access_denied
from psutil.tests import TRAVIS
from psutil.tests import unittest
from psutil.tests import wait_for_pid
from psutil.tests import which

def ps(fmt, pid=None):
    """
    Wrapper for calling the ps command with a little bit of cross-platform
    support for a narrow range of features.
    """
    cmd = [
     'ps']
    if LINUX:
        cmd.append('--no-headers')
    if pid is not None:
        cmd.extend(['-p', str(pid)])
    else:
        if SUNOS or AIX:
            cmd.append('-A')
        else:
            cmd.append('ax')
        if SUNOS:
            fmt_map = set(('command', 'comm', 'start', 'stime'))
            fmt = fmt_map.get(fmt, fmt)
        cmd.extend(['-o', fmt])
        output = sh(cmd)
        if LINUX:
            output = output.splitlines()
        else:
            output = output.splitlines()[1:]
    all_output = []
    for line in output:
        line = line.strip()
        try:
            line = int(line)
        except ValueError:
            pass

        all_output.append(line)

    if pid is None:
        return all_output
    else:
        return all_output[0]


def ps_name(pid):
    field = 'command'
    if SUNOS:
        field = 'comm'
    return ps(field, pid).split()[0]


def ps_args(pid):
    field = 'command'
    if AIX or SUNOS:
        field = 'args'
    return ps(field, pid)


def ps_rss(pid):
    field = 'rss'
    if AIX:
        field = 'rssize'
    return ps(field, pid)


def ps_vsz(pid):
    field = 'vsz'
    if AIX:
        field = 'vsize'
    return ps(field, pid)


@unittest.skipIf(not POSIX, 'POSIX only')
class TestProcess(unittest.TestCase):
    __doc__ = "Compare psutil results against 'ps' command line utility (mainly)."

    @classmethod
    def setUpClass(cls):
        cls.pid = get_test_subprocess([PYTHON_EXE, '-E', '-O'], stdin=subprocess.PIPE).pid
        wait_for_pid(cls.pid)

    @classmethod
    def tearDownClass(cls):
        reap_children()

    def test_ppid(self):
        ppid_ps = ps('ppid', self.pid)
        ppid_psutil = psutil.Process(self.pid).ppid()
        self.assertEqual(ppid_ps, ppid_psutil)

    def test_uid(self):
        uid_ps = ps('uid', self.pid)
        uid_psutil = psutil.Process(self.pid).uids().real
        self.assertEqual(uid_ps, uid_psutil)

    def test_gid(self):
        gid_ps = ps('rgid', self.pid)
        gid_psutil = psutil.Process(self.pid).gids().real
        self.assertEqual(gid_ps, gid_psutil)

    def test_username(self):
        username_ps = ps('user', self.pid)
        username_psutil = psutil.Process(self.pid).username()
        self.assertEqual(username_ps, username_psutil)

    def test_username_no_resolution(self):
        p = psutil.Process()
        with mock.patch('psutil.pwd.getpwuid', side_effect=KeyError) as (fun):
            self.assertEqual(p.username(), str(p.uids().real))
            assert fun.called

    @skip_on_access_denied()
    @retry_on_failure()
    def test_rss_memory(self):
        time.sleep(0.1)
        rss_ps = ps_rss(self.pid)
        rss_psutil = psutil.Process(self.pid).memory_info()[0] / 1024
        self.assertEqual(rss_ps, rss_psutil)

    @skip_on_access_denied()
    @retry_on_failure()
    def test_vsz_memory(self):
        time.sleep(0.1)
        vsz_ps = ps_vsz(self.pid)
        vsz_psutil = psutil.Process(self.pid).memory_info()[1] / 1024
        self.assertEqual(vsz_ps, vsz_psutil)

    def test_name(self):
        name_ps = ps_name(self.pid)
        name_ps = os.path.basename(name_ps).lower()
        name_psutil = psutil.Process(self.pid).name().lower()
        name_ps = re.sub('\\d.\\d', '', name_ps)
        name_psutil = re.sub('\\d.\\d', '', name_psutil)
        name_ps = re.sub('\\d', '', name_ps)
        name_psutil = re.sub('\\d', '', name_psutil)
        self.assertEqual(name_ps, name_psutil)

    def test_name_long(self):
        name = 'long-program-name'
        cmdline = ['long-program-name-extended', 'foo', 'bar']
        with mock.patch('psutil._psplatform.Process.name', return_value=name):
            with mock.patch('psutil._psplatform.Process.cmdline', return_value=cmdline):
                p = psutil.Process()
                self.assertEqual(p.name(), 'long-program-name-extended')

    def test_name_long_cmdline_ad_exc(self):
        name = 'long-program-name'
        with mock.patch('psutil._psplatform.Process.name', return_value=name):
            with mock.patch('psutil._psplatform.Process.cmdline', side_effect=psutil.AccessDenied(0, '')):
                p = psutil.Process()
                self.assertEqual(p.name(), 'long-program-name')

    def test_name_long_cmdline_nsp_exc(self):
        name = 'long-program-name'
        with mock.patch('psutil._psplatform.Process.name', return_value=name):
            with mock.patch('psutil._psplatform.Process.cmdline', side_effect=psutil.NoSuchProcess(0, '')):
                p = psutil.Process()
                self.assertRaises(psutil.NoSuchProcess, p.name)

    @unittest.skipIf(MACOS or BSD, 'ps -o start not available')
    def test_create_time(self):
        time_ps = ps('start', self.pid)
        time_psutil = psutil.Process(self.pid).create_time()
        time_psutil_tstamp = datetime.datetime.fromtimestamp(time_psutil).strftime('%H:%M:%S')
        round_time_psutil = round(time_psutil)
        round_time_psutil_tstamp = datetime.datetime.fromtimestamp(round_time_psutil).strftime('%H:%M:%S')
        self.assertIn(time_ps, [time_psutil_tstamp, round_time_psutil_tstamp])

    def test_exe(self):
        ps_pathname = ps_name(self.pid)
        psutil_pathname = psutil.Process(self.pid).exe()
        try:
            self.assertEqual(ps_pathname, psutil_pathname)
        except AssertionError:
            adjusted_ps_pathname = ps_pathname[:len(ps_pathname)]
            self.assertEqual(ps_pathname, adjusted_ps_pathname)

    def test_cmdline(self):
        ps_cmdline = ps_args(self.pid)
        psutil_cmdline = ' '.join(psutil.Process(self.pid).cmdline())
        self.assertEqual(ps_cmdline, psutil_cmdline)

    @unittest.skipIf(SUNOS, 'not reliable on SUNOS')
    @unittest.skipIf(AIX, 'not reliable on AIX')
    def test_nice(self):
        ps_nice = ps('nice', self.pid)
        psutil_nice = psutil.Process().nice()
        self.assertEqual(ps_nice, psutil_nice)

    def test_num_fds(self):

        def call(p, attr):
            args = ()
            attr = getattr(p, name, None)
            if attr is not None and callable(attr):
                if name == 'rlimit':
                    args = (
                     psutil.RLIMIT_NOFILE,)
                attr(*args)
            else:
                attr

        p = psutil.Process(os.getpid())
        failures = []
        ignored_names = ['terminate', 'kill', 'suspend', 'resume', 'nice',
         'send_signal', 'wait', 'children', 'as_dict',
         'memory_info_ex', 'parent', 'parents']
        if LINUX and get_kernel_version() < (2, 6, 36):
            ignored_names.append('rlimit')
        if LINUX and get_kernel_version() < (2, 6, 23):
            ignored_names.append('num_ctx_switches')
        for name in dir(psutil.Process):
            if not name.startswith('_'):
                if name in ignored_names:
                    continue
                else:
                    try:
                        num1 = p.num_fds()
                        for x in range(2):
                            call(p, name)

                        num2 = p.num_fds()
                    except psutil.AccessDenied:
                        pass
                    else:
                        if abs(num2 - num1) > 1:
                            fail = 'failure while processing Process.%s method (before=%s, after=%s)' % (
                             name, num1, num2)
                            failures.append(fail)

        if failures:
            self.fail('\n' + '\n'.join(failures))


@unittest.skipIf(not POSIX, 'POSIX only')
class TestSystemAPIs(unittest.TestCase):
    __doc__ = 'Test some system APIs.'

    @retry_on_failure()
    def test_pids(self):
        pids_ps = sorted(ps('pid'))
        pids_psutil = psutil.pids()
        if MACOS or OPENBSD and 0 not in pids_ps:
            pids_ps.insert(0, 0)
        if len(pids_ps) - len(pids_psutil) > 1:
            difference = [x for x in pids_psutil if x not in pids_ps] + [x for x in pids_ps if x not in pids_psutil]
            self.fail('difference: ' + str(difference))

    @unittest.skipIf(SUNOS, 'unreliable on SUNOS')
    @unittest.skipIf(TRAVIS, 'unreliable on TRAVIS')
    @unittest.skipIf(not which('ifconfig'), 'no ifconfig cmd')
    @unittest.skipIf(not HAS_NET_IO_COUNTERS, 'not supported')
    def test_nic_names(self):
        output = sh('ifconfig -a')
        for nic in psutil.net_io_counters(pernic=True).keys():
            for line in output.split():
                if line.startswith(nic):
                    break
            else:
                self.fail("couldn't find %s nic in 'ifconfig -a' output\n%s" % (
                 nic, output))

    @unittest.skipIf(CI_TESTING and not psutil.users(), 'unreliable on CI')
    @retry_on_failure()
    def test_users(self):
        out = sh('who')
        lines = out.split('\n')
        if not lines:
            raise self.skipTest('no users on this system')
        users = [x.split()[0] for x in lines]
        terminals = [x.split()[1] for x in lines]
        self.assertEqual(len(users), len(psutil.users()))
        for u in psutil.users():
            self.assertIn(u.name, users)
            self.assertIn(u.terminal, terminals)

    def test_pid_exists_let_raise(self):
        with mock.patch('psutil._psposix.os.kill', side_effect=OSError(errno.EBADF, '')) as (m):
            self.assertRaises(OSError, psutil._psposix.pid_exists, os.getpid())
            assert m.called

    def test_os_waitpid_let_raise(self):
        with mock.patch('psutil._psposix.os.waitpid', side_effect=OSError(errno.EBADF, '')) as (m):
            self.assertRaises(OSError, psutil._psposix.wait_pid, os.getpid())
            assert m.called

    def test_os_waitpid_eintr(self):
        with mock.patch('psutil._psposix.os.waitpid', side_effect=OSError(errno.EINTR, '')) as (m):
            self.assertRaises(psutil._psposix.TimeoutExpired, psutil._psposix.wait_pid, os.getpid(), timeout=0.01)
            assert m.called

    def test_os_waitpid_bad_ret_status(self):
        with mock.patch('psutil._psposix.os.waitpid', return_value=(1, -1)) as (m):
            self.assertRaises(ValueError, psutil._psposix.wait_pid, os.getpid())
            assert m.called

    @unittest.skipIf(AIX, 'unreliable on AIX')
    def test_disk_usage(self):

        def df(device):
            out = sh('df -k %s' % device).strip()
            line = out.split('\n')[1]
            fields = line.split()
            total = int(fields[1]) * 1024
            used = int(fields[2]) * 1024
            free = int(fields[3]) * 1024
            percent = float(fields[4].replace('%', ''))
            return (total, used, free, percent)

        tolerance = 4194304
        for part in psutil.disk_partitions(all=False):
            usage = psutil.disk_usage(part.mountpoint)
            try:
                total, used, free, percent = df(part.device)
            except RuntimeError as err:
                err = str(err).lower()
                if 'no such file or directory' in err or 'raw devices not supported' in err or 'permission denied' in err:
                    continue
                else:
                    raise
            else:
                self.assertAlmostEqual(usage.total, total, delta=tolerance)
                self.assertAlmostEqual(usage.used, used, delta=tolerance)
                self.assertAlmostEqual(usage.free, free, delta=tolerance)
                self.assertAlmostEqual(usage.percent, percent, delta=1)


if __name__ == '__main__':
    from psutil.tests.runner import run
    run(__file__)