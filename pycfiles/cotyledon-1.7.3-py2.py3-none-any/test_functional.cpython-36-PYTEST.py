# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /workspace/sileht/common/cotyledon/build/lib.linux-x86_64-2.7/cotyledon/tests/test_functional.py
# Compiled at: 2018-08-28 05:24:33
# Size of source mod 2**32: 15681 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, re, signal, socket, subprocess, threading, time, unittest
from cotyledon import oslo_config_glue
from cotyledon.tests import base
if os.name == 'posix':

    def pid_exists(pid):
        """Check whether pid exists in the current process table."""
        import errno
        if pid < 0:
            return False
        try:
            os.kill(pid, 0)
        except OSError as e:
            return e.errno == errno.EPERM
        else:
            return True


else:

    def pid_exists(pid):
        import ctypes
        kernel32 = ctypes.windll.kernel32
        SYNCHRONIZE = 1048576
        process = kernel32.OpenProcess(SYNCHRONIZE, 0, pid)
        if process != 0:
            kernel32.CloseHandle(process)
            return True
        else:
            return False


class Base(base.TestCase):

    def setUp(self):
        super(Base, self).setUp()
        self.lines = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('127.0.0.1', 0))
        self.t = threading.Thread(target=(self.readlog))
        self.t.daemon = True
        self.t.start()
        examplepy = os.path.join(os.path.dirname(__file__), 'examples.py')
        if os.name == 'posix':
            kwargs = {'preexec_fn': os.setsid}
        else:
            kwargs = {'creationflags': subprocess.CREATE_NEW_PROCESS_GROUP}
        self.subp = (subprocess.Popen)(
         ['python', examplepy, self.name,
          str(self.sock.getsockname()[1])], **kwargs)

    def readlog(self):
        try:
            while True:
                data, addr = self.sock.recvfrom(65565)
                self.lines.append(data.strip())

        except socket.error:
            pass

    def tearDown(self):
        if self.subp.poll() is None:
            self.subp.kill()
        super(Base, self).tearDown()

    def get_lines(self, number=None):
        if number is not None:
            while len(self.lines) < number:
                time.sleep(0.1)

            lines = self.lines[:number]
            del self.lines[:number]
            return lines
        else:
            self.subp.wait()
            return self.lines

    @staticmethod
    def hide_pids(lines):
        return [re.sub(b'Child \\d+', b'Child XXXX', re.sub(b' \\[[^\\]]*\\]', b' [XXXX]', line)) for line in lines]

    @staticmethod
    def get_pid(line):
        try:
            return int(line.split()[(-1)][1:-1])
        except Exception:
            raise Exception('Fail to find pid in %s' % line.split())


class TestCotyledon(Base):
    name = 'example_app'

    def assert_everything_has_started(self):
        lines = sorted(self.get_lines(7))
        self.pid_heavy_1 = self.get_pid(lines[0])
        self.pid_heavy_2 = self.get_pid(lines[1])
        self.pid_light_1 = self.get_pid(lines[2])
        lines = self.hide_pids(lines)
        self.assertEqual([
         b'DEBUG:cotyledon._service:Run service heavy(0) [XXXX]',
         b'DEBUG:cotyledon._service:Run service heavy(1) [XXXX]',
         b'DEBUG:cotyledon._service:Run service light(0) [XXXX]',
         b'ERROR:cotyledon.tests.examples:heavy init',
         b'ERROR:cotyledon.tests.examples:heavy init',
         b'ERROR:cotyledon.tests.examples:heavy run',
         b'ERROR:cotyledon.tests.examples:heavy run'], lines)
        self.assert_everything_is_alive()

    def assert_everything_is_alive(self):
        self.assertTrue(pid_exists(self.subp.pid))
        self.assertTrue(pid_exists(self.pid_light_1))
        self.assertTrue(pid_exists(self.pid_heavy_1))
        self.assertTrue(pid_exists(self.pid_heavy_2))

    def assert_everything_is_dead(self, status=0):
        self.assertEqual(status, self.subp.poll())
        self.assertFalse(pid_exists(self.subp.pid))
        self.assertFalse(pid_exists(self.pid_light_1))
        self.assertFalse(pid_exists(self.pid_heavy_1))
        self.assertFalse(pid_exists(self.pid_heavy_2))

    @unittest.skipIf(os.name == 'posix', 'no window support')
    def test_workflow_window(self):
        self.assert_everything_has_started()
        os.kill(self.pid_heavy_1, signal.SIGTERM)
        lines = self.get_lines(4)
        lines = self.hide_pids(lines)
        self.assertEqual([
         b'INFO:cotyledon._service_manager:Child XXXX exited with status 15',
         b'ERROR:cotyledon.tests.examples:heavy init',
         b'DEBUG:cotyledon._service:Run service heavy(0) [XXXX]',
         b'ERROR:cotyledon.tests.examples:heavy run'], lines)
        os.kill(self.subp.pid, signal.SIGTERM)
        time.sleep(1)
        lines = self.get_lines()
        lines = sorted(self.hide_pids(lines))
        self.assertEqual([
         b'ERROR:cotyledon.tests.examples:heavy terminate',
         b'ERROR:cotyledon.tests.examples:heavy terminate',
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service heavy(0) [XXXX]',
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service heavy(1) [XXXX]',
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service light(0) [XXXX]',
         b'INFO:cotyledon._service:Parent process has died unexpectedly, heavy(0) [XXXX] exiting',
         b'INFO:cotyledon._service:Parent process has died unexpectedly, heavy(1) [XXXX] exiting',
         b'INFO:cotyledon._service:Parent process has died unexpectedly, light(0) [XXXX] exiting'], lines)
        self.assertEqual(15, self.subp.poll())

    @unittest.skipIf(os.name != 'posix', 'no posix support')
    def test_workflow(self):
        self.assert_everything_has_started()
        os.kill(self.pid_heavy_1, signal.SIGHUP)
        self.assertEqual([b'ERROR:cotyledon.tests.examples:heavy reload'], self.get_lines(1))
        os.kill(self.pid_light_1, signal.SIGHUP)
        lines = self.get_lines(3)
        self.pid_light_1 = self.get_pid(lines[(-1)])
        lines = self.hide_pids(lines)
        self.assertEqual([
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service light(0) [XXXX]',
         b'INFO:cotyledon._service_manager:Child XXXX exited with status 0',
         b'DEBUG:cotyledon._service:Run service light(0) [XXXX]'], lines)
        os.kill(self.pid_heavy_1, signal.SIGTERM)
        lines = self.get_lines(6)
        self.pid_heavy_1 = self.get_pid(lines[(-2)])
        lines = self.hide_pids(lines)
        self.assertEqual([
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service heavy(0) [XXXX]',
         b'ERROR:cotyledon.tests.examples:heavy terminate',
         b'INFO:cotyledon._service_manager:Child XXXX exited with status 42',
         b'ERROR:cotyledon.tests.examples:heavy init',
         b'DEBUG:cotyledon._service:Run service heavy(0) [XXXX]',
         b'ERROR:cotyledon.tests.examples:heavy run'], lines)
        os.kill(self.pid_light_1, signal.SIGTERM)
        lines = self.get_lines(3)
        self.pid_light_1 = self.get_pid(lines[(-1)])
        lines = self.hide_pids(lines)
        self.assertEqual([
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service light(0) [XXXX]',
         b'INFO:cotyledon._service_manager:Child XXXX exited with status 0',
         b'DEBUG:cotyledon._service:Run service light(0) [XXXX]'], lines)
        self.assert_everything_is_alive()
        os.kill(self.subp.pid, signal.SIGTERM)
        lines = self.get_lines()
        self.assertEqual(b'DEBUG:cotyledon._service_manager:Shutdown finish', lines[(-1)])
        time.sleep(1)
        lines = sorted(self.hide_pids(lines))
        self.assertEqual([
         b'DEBUG:cotyledon._service_manager:Killing services with signal SIGTERM',
         b'DEBUG:cotyledon._service_manager:Shutdown finish',
         b'DEBUG:cotyledon._service_manager:Waiting services to terminate',
         b'ERROR:cotyledon.tests.examples:heavy terminate',
         b'ERROR:cotyledon.tests.examples:heavy terminate',
         b'ERROR:cotyledon.tests.examples:master terminate hook',
         b'ERROR:cotyledon.tests.examples:master terminate2 hook',
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service heavy(0) [XXXX]',
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service heavy(1) [XXXX]',
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service light(0) [XXXX]',
         b'INFO:cotyledon._service_manager:Caught SIGTERM signal, graceful exiting of master process'], lines)
        self.assert_everything_is_dead()

    @unittest.skipIf(os.name != 'posix', 'http://bugs.python.org/issue18040')
    def test_sigint(self):
        self.assert_everything_has_started()
        os.kill(self.subp.pid, signal.SIGINT)
        time.sleep(1)
        lines = sorted(self.get_lines())
        lines = self.hide_pids(lines)
        self.assertEqual([
         b'INFO:cotyledon._service_manager:Caught SIGINT signal, instantaneous exiting'], lines)
        self.assert_everything_is_dead(1)

    @unittest.skipIf(os.name != 'posix', 'no posix support')
    def test_sighup(self):
        self.assert_everything_has_started()
        os.kill(self.subp.pid, signal.SIGHUP)
        time.sleep(0.5)
        lines = sorted(self.get_lines(6))
        lines = self.hide_pids(lines)
        self.assertEqual([
         b'DEBUG:cotyledon._service:Run service light(0) [XXXX]',
         b'ERROR:cotyledon.tests.examples:heavy reload',
         b'ERROR:cotyledon.tests.examples:heavy reload',
         b'ERROR:cotyledon.tests.examples:master reload hook',
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service light(0) [XXXX]',
         b'INFO:cotyledon._service_manager:Child XXXX exited with status 0'], lines)
        os.kill(self.subp.pid, signal.SIGINT)
        time.sleep(0.5)
        self.assert_everything_is_dead(1)

    @unittest.skipIf(os.name != 'posix', 'no posix support')
    def test_sigkill(self):
        self.assert_everything_has_started()
        self.subp.kill()
        time.sleep(1)
        lines = sorted(self.get_lines())
        lines = self.hide_pids(lines)
        self.assertEqual([
         b'ERROR:cotyledon.tests.examples:heavy terminate',
         b'ERROR:cotyledon.tests.examples:heavy terminate',
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service heavy(0) [XXXX]',
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service heavy(1) [XXXX]',
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service light(0) [XXXX]',
         b'INFO:cotyledon._service:Parent process has died unexpectedly, heavy(0) [XXXX] exiting',
         b'INFO:cotyledon._service:Parent process has died unexpectedly, heavy(1) [XXXX] exiting',
         b'INFO:cotyledon._service:Parent process has died unexpectedly, light(0) [XXXX] exiting'], lines)
        self.assert_everything_is_dead(-9)


class TestBadlyCodedCotyledon(Base):
    name = 'badly_coded_app'

    @unittest.skipIf(os.name != 'posix', 'no posix support')
    def test_badly_coded(self):
        time.sleep(0.5)
        self.subp.terminate()
        time.sleep(0.5)
        self.assertEqual(0, self.subp.poll(), self.get_lines())
        self.assertFalse(pid_exists(self.subp.pid))


class TestBuggyCotyledon(Base):
    name = 'buggy_app'

    @unittest.skipIf(os.name != 'posix', 'no posix support')
    def test_graceful_timeout_term(self):
        lines = self.get_lines(1)
        childpid = self.get_pid(lines[0])
        self.subp.terminate()
        time.sleep(2)
        self.assertEqual(0, self.subp.poll())
        self.assertFalse(pid_exists(self.subp.pid))
        self.assertFalse(pid_exists(childpid))
        lines = self.hide_pids(self.get_lines())
        self.assertNotIn('ERROR:cotyledon.tests.examples:time.sleep done', lines)
        self.assertEqual([
         b'INFO:cotyledon._service:Graceful shutdown timeout (1) exceeded, exiting buggy(0) [XXXX] now.',
         b'DEBUG:cotyledon._service_manager:Shutdown finish'], lines[-2:])

    @unittest.skipIf(os.name != 'posix', 'no posix support')
    def test_graceful_timeout_kill(self):
        lines = self.get_lines(1)
        childpid = self.get_pid(lines[0])
        self.subp.kill()
        time.sleep(2)
        self.assertEqual(-9, self.subp.poll())
        self.assertFalse(pid_exists(self.subp.pid))
        self.assertFalse(pid_exists(childpid))
        lines = self.hide_pids(self.get_lines())
        self.assertNotIn('ERROR:cotyledon.tests.examples:time.sleep done', lines)
        self.assertEqual([
         b'INFO:cotyledon._service:Parent process has died unexpectedly, buggy(0) [XXXX] exiting',
         b'INFO:cotyledon._service:Caught SIGTERM signal, graceful exiting of service buggy(0) [XXXX]',
         b'INFO:cotyledon._service:Graceful shutdown timeout (1) exceeded, exiting buggy(0) [XXXX] now.'], lines[-3:])


class TestOsloCotyledon(Base):
    name = 'oslo_app'

    def test_options(self):
        options = oslo_config_glue.list_opts()
        self.assertEqual(1, len(options))
        self.assertEqual(None, options[0][0])
        self.assertEqual(2, len(options[0][1]))
        lines = self.get_lines(1)
        self.assertIn(b'DEBUG:cotyledon.oslo_config_glue:Full set of CONF:', lines)
        self.subp.terminate()