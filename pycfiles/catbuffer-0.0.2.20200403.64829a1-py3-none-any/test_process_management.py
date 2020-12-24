# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./tests/test_process_management.py
# Compiled at: 2014-04-22 14:05:22
import os, signal, sys, subprocess, time, testing, testify as T

class ProcessManagementTestCase(testing.BaseTestCase):

    def test_child(self):
        """catbox.run will fork(). Child process will execute
        self.child_function. This test verifies that child is actually
        running the given function reporting back to parent through a
        Unix pipe.
        """
        self.run_child_function_in_catbox()
        self.verify_message_from_child()

    def test_child_does_not_report_back(self):

        def lazy_child():
            pass

        with T.assert_raises(testing.ChildDidNotReportBackException):
            self.run_child_function_in_catbox(lazy_child)
            self.verify_message_from_child()

    def test_subprocess_kill(self):
        """Verify that killing the subprocess in the forked process
        will not have side effects on catbox.
        """

        def child_calling_subprocess_kill():
            sleep_time = 5
            start_time = time.time()
            sub = subprocess.Popen(['/bin/sleep', '%d' % sleep_time], stdout=subprocess.PIPE)
            sub.kill()
            sub.wait()
            elapsed_time = time.time() - start_time
            assert elapsed_time < sleep_time
            os.write(self.write_pipe, self.default_expected_message_from_child)

        self.run_child_function_in_catbox(child_function=child_calling_subprocess_kill)
        self.verify_message_from_child()


class WatchdogTestCase(testing.BaseTestCase):

    def test_watchdog(self):

        def sleeping_child_function():
            time.sleep(5)

        child_processes = []
        catbox_pid = os.fork()
        if not catbox_pid:
            self.run_child_function_in_catbox(child_function=sleeping_child_function)
            assert False, "Shouldn't get here. Parent should kill us already."
            sys.exit(0)
        else:
            time.sleep(0.1)
            child_processes = testing.child_processes(catbox_pid)
            os.kill(catbox_pid, signal.SIGKILL)
            os.waitpid(catbox_pid, 0)
        time.sleep(0.1)
        T.assert_equal(testing.is_process_alive(catbox_pid), False, 'Catbox process (%d) is still running' % catbox_pid)
        for pid in child_processes:
            pid = int(pid)
            T.assert_equal(testing.is_process_alive(pid), False, 'Child process (%d) is still running' % pid)