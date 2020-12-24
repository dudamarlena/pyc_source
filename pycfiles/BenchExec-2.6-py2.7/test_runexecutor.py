# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/test_runexecutor.py
# Compiled at: 2020-05-07 05:52:35
from __future__ import absolute_import, division, print_function, unicode_literals
import glob, logging, os, re, subprocess, sys, tempfile, threading, time, unittest, shutil
from benchexec import container
from benchexec import containerexecutor
from benchexec import filehierarchylimit
from benchexec.runexecutor import RunExecutor
from benchexec import runexecutor
from benchexec import util
sys.dont_write_bytecode = True
try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, b'wb')

try:
    unichr(0)
except NameError:
    unichr = chr

here = os.path.dirname(__file__)
base_dir = os.path.join(here, b'..')
bin_dir = os.path.join(base_dir, b'bin')
runexec = os.path.join(bin_dir, b'runexec')
if sys.version_info[0] == 2:
    python = b'python2'
    trivial_run_grace_time = 0.4
else:
    python = b'python3'
    trivial_run_grace_time = 0.2

class TestRunExecutor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.longMessage = True
        cls.maxDiff = None
        logging.disable(logging.CRITICAL)
        if not hasattr(cls, b'assertRegex'):
            cls.assertRegex = cls.assertRegexpMatches
        if not hasattr(cls, b'assertRaisesRegex'):
            cls.assertRaisesRegex = cls.assertRaisesRegexp
        return

    def setUp(self, *args, **kwargs):
        try:
            self.runexecutor = RunExecutor(use_namespaces=False, *args, **kwargs)
        except SystemExit as e:
            if str(e).startswith(b'Cannot reliably kill sub-processes without freezer cgroup'):
                self.skipTest(e)
            else:
                raise e

    def execute_run(self, *args, **kwargs):
        expect_terminationreason = kwargs.pop(b'expect_terminationreason', None)
        output_fd, output_filename = tempfile.mkstemp(b'.log', b'output_', text=True)
        try:
            result = self.runexecutor.execute_run(list(args), output_filename, **kwargs)
            output = os.read(output_fd, 4096).decode()
        finally:
            os.close(output_fd)
            os.remove(output_filename)

        self.check_result_keys(result, b'terminationreason')
        if isinstance(expect_terminationreason, list):
            self.assertIn(result.get(b'terminationreason'), expect_terminationreason, b'Unexpected terminationreason, output is \n' + output)
        else:
            self.assertEqual(result.get(b'terminationreason'), expect_terminationreason, b'Unexpected terminationreason, output is \n' + output)
        return (result, output.splitlines())

    def get_runexec_cmdline(self, *args, **kwargs):
        return [
         python,
         runexec,
         b'--no-container',
         b'--output',
         kwargs[b'output_filename']] + list(args)

    def execute_run_extern(self, *args, **kwargs):
        expect_terminationreason = kwargs.pop(b'expect_terminationreason', None)
        output_fd, output_filename = tempfile.mkstemp(b'.log', b'output_', text=True)
        try:
            try:
                runexec_output = subprocess.check_output(args=self.get_runexec_cmdline(output_filename=output_filename, *args), stderr=DEVNULL, **kwargs).decode()
                output = os.read(output_fd, 4096).decode()
            except subprocess.CalledProcessError as e:
                print(e.output.decode())
                raise e

        finally:
            os.close(output_fd)
            os.remove(output_filename)

        result = {key.strip():value.strip() for key, _, value in (line.partition(b'=') for line in runexec_output.splitlines())}
        self.check_result_keys(result, b'terminationreason', b'returnvalue')
        if isinstance(expect_terminationreason, list):
            self.assertIn(result.get(b'terminationreason'), expect_terminationreason, b'Unexpected terminationreason, output is \n' + output)
        else:
            self.assertEqual(result.get(b'terminationreason'), expect_terminationreason, b'Unexpected terminationreason, output is \n' + output)
        return (result, output.splitlines())

    def check_command_in_output(self, output, cmd):
        self.assertEqual(output[0], cmd, b'run output misses executed command')

    def check_result_keys(self, result, *additional_keys):
        expected_keys = {
         b'cputime',
         b'walltime',
         b'memory',
         b'exitcode',
         b'cpuenergy',
         b'blkio-read',
         b'blkio-write',
         b'starttime'}
        expected_keys.update(additional_keys)
        for key in result.keys():
            if key.startswith(b'cputime-cpu'):
                self.assertRegex(key, b'^cputime-cpu[0-9]+$', (b"unexpected result entry '{}={}'").format(key, result[key]))
            elif key.startswith(b'cpuenergy-'):
                self.assertRegex(key, b'^cpuenergy-pkg[0-9]+(-(core|uncore|dram|psys))?$', (b"unexpected result entry '{}={}'").format(key, result[key]))
            else:
                self.assertIn(key, expected_keys, (b"unexpected result entry '{}={}'").format(key, result[key]))

    def check_exitcode(self, result, exitcode, msg=None):
        self.assertEqual(result[b'exitcode'].raw, exitcode, msg)

    def check_exitcode_extern(self, result, exitcode, msg=None):
        exitcode = util.ProcessExitCode.from_raw(exitcode)
        if exitcode.value is not None:
            self.assertEqual(int(result[b'returnvalue']), exitcode.value, msg)
        else:
            self.assertEqual(int(result[b'exitsignal']), exitcode.signal, msg)
        return

    def test_command_output(self):
        if not os.path.exists(b'/bin/echo'):
            self.skipTest(b'missing /bin/echo')
        _, output = self.execute_run(b'/bin/echo', b'TEST_TOKEN')
        self.check_command_in_output(output, b'/bin/echo TEST_TOKEN')
        self.assertEqual(output[(-1)], b'TEST_TOKEN', b'run output misses command output')
        for line in output[1:-1]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

    def test_command_error_output(self):
        if not os.path.exists(b'/bin/echo'):
            self.skipTest(b'missing /bin/echo')
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')

        def execute_Run_intern(*args, **kwargs):
            error_fd, error_filename = tempfile.mkstemp(b'.log', b'error_', text=True)
            try:
                _, output_lines = self.execute_run(error_filename=error_filename, *args, **kwargs)
                error_lines = os.read(error_fd, 4096).decode().splitlines()
                return (output_lines, error_lines)
            finally:
                os.close(error_fd)
                os.remove(error_filename)

        output_lines, error_lines = execute_Run_intern(b'/bin/sh', b'-c', b'/bin/echo ERROR_TOKEN >&2')
        self.assertEqual(error_lines[(-1)], b'ERROR_TOKEN', b'run error output misses command output')
        for line in output_lines[1:]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

        for line in error_lines[1:-1]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run error output')

        output_lines, error_lines = execute_Run_intern(b'/bin/echo', b'OUT_TOKEN')
        self.check_command_in_output(output_lines, b'/bin/echo OUT_TOKEN')
        self.check_command_in_output(error_lines, b'/bin/echo OUT_TOKEN')
        self.assertEqual(output_lines[(-1)], b'OUT_TOKEN', b'run output misses command output')
        for line in output_lines[1:-1]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

        for line in error_lines[1:]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run error output')

    def test_command_result(self):
        if not os.path.exists(b'/bin/echo'):
            self.skipTest(b'missing /bin/echo')
        result, _ = self.execute_run(b'/bin/echo', b'TEST_TOKEN')
        self.check_exitcode(result, 0, b'exit code of /bin/echo is not zero')
        self.assertAlmostEqual(result[b'walltime'], trivial_run_grace_time, delta=trivial_run_grace_time, msg=b'walltime of /bin/echo not as expected')
        if b'cputime' in result:
            self.assertAlmostEqual(result[b'cputime'], trivial_run_grace_time, delta=trivial_run_grace_time, msg=b'cputime of /bin/echo not as expected')
        self.check_result_keys(result)

    def test_wrong_command(self):
        result, _ = self.execute_run(b'/does/not/exist', expect_terminationreason=b'failed')

    def test_wrong_command_extern(self):
        result, _ = self.execute_run(b'/does/not/exist', expect_terminationreason=b'failed')

    def test_cputime_hardlimit(self):
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')
        try:
            result, output = self.execute_run(b'/bin/sh', b'-c', b'i=0; while [ $i -lt 10000000 ]; do i=$(($i+1)); done; echo $i', hardtimelimit=1, expect_terminationreason=b'cputime')
        except SystemExit as e:
            self.assertEqual(str(e), b'Time limit cannot be specified without cpuacct cgroup.')
            self.skipTest(e)

        self.check_exitcode(result, 9, b'exit code of killed process is not 9')
        self.assertAlmostEqual(result[b'walltime'], 1.4, delta=0.5, msg=b'walltime is not approximately the time after which the process should have been killed')
        self.assertAlmostEqual(result[b'cputime'], 1.4, delta=0.5, msg=b'cputime is not approximately the time after which the process should have been killed')
        for line in output[1:]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

    def test_cputime_softlimit(self):
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')
        try:
            result, output = self.execute_run(b'/bin/sh', b'-c', b'i=0; while [ $i -lt 10000000 ]; do i=$(($i+1)); done; echo $i', softtimelimit=1, expect_terminationreason=b'cputime-soft')
        except SystemExit as e:
            self.assertEqual(str(e), b'Soft time limit cannot be specified without cpuacct cgroup.')
            self.skipTest(e)

        self.check_exitcode(result, 15, b'exit code of killed process is not 15')
        self.assertAlmostEqual(result[b'walltime'], 4, delta=3, msg=b'walltime is not approximately the time after which the process should have been killed')
        self.assertAlmostEqual(result[b'cputime'], 4, delta=3, msg=b'cputime is not approximately the time after which the process should have been killed')
        for line in output[1:]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

    def test_walltime_limit(self):
        if not os.path.exists(b'/bin/sleep'):
            self.skipTest(b'missing /bin/sleep')
        result, output = self.execute_run(b'/bin/sleep', b'10', walltimelimit=1, expect_terminationreason=b'walltime')
        self.check_exitcode(result, 9, b'exit code of killed process is not 9')
        self.assertAlmostEqual(result[b'walltime'], 4, delta=3, msg=b'walltime is not approximately the time after which the process should have been killed')
        if b'cputime' in result:
            self.assertAlmostEqual(result[b'cputime'], trivial_run_grace_time, delta=trivial_run_grace_time, msg=b'cputime of /bin/sleep is not approximately zero')
        self.check_command_in_output(output, b'/bin/sleep 10')
        for line in output[1:]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

    def test_cputime_walltime_limit(self):
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')
        try:
            result, output = self.execute_run(b'/bin/sh', b'-c', b'i=0; while [ $i -lt 10000000 ]; do i=$(($i+1)); done; echo $i', hardtimelimit=1, walltimelimit=5, expect_terminationreason=b'cputime')
        except SystemExit as e:
            self.assertEqual(str(e), b'Time limit cannot be specified without cpuacct cgroup.')
            self.skipTest(e)

        self.check_exitcode(result, 9, b'exit code of killed process is not 9')
        self.assertAlmostEqual(result[b'walltime'], 1.4, delta=0.5, msg=b'walltime is not approximately the time after which the process should have been killed')
        self.assertAlmostEqual(result[b'cputime'], 1.4, delta=0.5, msg=b'cputime is not approximately the time after which the process should have been killed')
        for line in output[1:]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

    def test_all_timelimits(self):
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')
        try:
            result, output = self.execute_run(b'/bin/sh', b'-c', b'i=0; while [ $i -lt 10000000 ]; do i=$(($i+1)); done; echo $i', softtimelimit=1, hardtimelimit=2, walltimelimit=5, expect_terminationreason=b'cputime-soft')
        except SystemExit as e:
            self.assertEqual(str(e), b'Time limit cannot be specified without cpuacct cgroup.')
            self.skipTest(e)

        self.check_exitcode(result, 15, b'exit code of killed process is not 15')
        self.assertAlmostEqual(result[b'walltime'], 1.4, delta=0.5, msg=b'walltime is not approximately the time after which the process should have been killed')
        self.assertAlmostEqual(result[b'cputime'], 1.4, delta=0.5, msg=b'cputime is not approximately the time after which the process should have been killed')
        for line in output[1:]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

    def test_input_is_redirected_from_devnull(self):
        if not os.path.exists(b'/bin/cat'):
            self.skipTest(b'missing /bin/cat')
        result, output = self.execute_run(b'/bin/cat', walltimelimit=1)
        self.check_exitcode(result, 0, b'exit code of process is not 0')
        self.assertAlmostEqual(result[b'walltime'], trivial_run_grace_time, delta=trivial_run_grace_time, msg=b'walltime of "/bin/cat < /dev/null" is not approximately zero')
        if b'cputime' in result:
            self.assertAlmostEqual(result[b'cputime'], trivial_run_grace_time, delta=trivial_run_grace_time, msg=b'cputime of "/bin/cat < /dev/null" is not approximately zero')
        self.check_result_keys(result)
        self.check_command_in_output(output, b'/bin/cat')
        for line in output[1:]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

    def test_input_is_redirected_from_file(self):
        if not os.path.exists(b'/bin/cat'):
            self.skipTest(b'missing /bin/cat')
        with tempfile.TemporaryFile() as (tmp):
            tmp.write(b'TEST_TOKEN')
            tmp.flush()
            tmp.seek(0)
            result, output = self.execute_run(b'/bin/cat', stdin=tmp, walltimelimit=1)
        self.check_exitcode(result, 0, b'exit code of process is not 0')
        self.assertAlmostEqual(result[b'walltime'], trivial_run_grace_time, delta=trivial_run_grace_time, msg=b'walltime of "/bin/cat < /dev/null" is not approximately zero')
        if b'cputime' in result:
            self.assertAlmostEqual(result[b'cputime'], trivial_run_grace_time, delta=trivial_run_grace_time, msg=b'cputime of "/bin/cat < /dev/null" is not approximately zero')
        self.check_result_keys(result)
        self.check_command_in_output(output, b'/bin/cat')
        self.assertEqual(output[(-1)], b'TEST_TOKEN', b'run output misses command output')
        for line in output[1:-1]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

    def test_input_is_redirected_from_stdin(self):
        if not os.path.exists(b'/bin/cat'):
            self.skipTest(b'missing /bin/cat')
        output_fd, output_filename = tempfile.mkstemp(b'.log', b'output_', text=True)
        cmd = self.get_runexec_cmdline(b'--input', b'-', b'--walltime', b'1', b'/bin/cat', output_filename=output_filename)
        try:
            process = subprocess.Popen(args=cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=DEVNULL)
            try:
                runexec_output, unused_err = process.communicate(b'TEST_TOKEN')
            except:
                process.kill()
                process.wait()
                raise

            retcode = process.poll()
            if retcode:
                print(runexec_output.decode())
                raise subprocess.CalledProcessError(retcode, cmd, output=runexec_output)
            output = os.read(output_fd, 4096).decode().splitlines()
        finally:
            os.close(output_fd)
            os.remove(output_filename)

        result = {key.strip():value.strip() for key, _, value in (line.partition(b'=') for line in runexec_output.decode().splitlines())}
        self.check_exitcode_extern(result, 0, b'exit code of process is not 0')
        self.assertAlmostEqual(float(result[b'walltime'].rstrip(b's')), trivial_run_grace_time, delta=trivial_run_grace_time, msg=b'walltime of "/bin/cat < /dev/null" is not approximately zero')
        if b'cputime' in result:
            self.assertAlmostEqual(float(result[b'cputime'].rstrip(b's')), trivial_run_grace_time, delta=trivial_run_grace_time, msg=b'cputime of "/bin/cat < /dev/null" is not approximately zero')
        self.check_result_keys(result, b'returnvalue')
        self.check_command_in_output(output, b'/bin/cat')
        self.assertEqual(output[(-1)], b'TEST_TOKEN', b'run output misses command output')
        for line in output[1:-1]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

    def test_append_environment_variable(self):
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')
        _, output = self.execute_run(b'/bin/sh', b'-c', b'echo $PATH')
        path = output[(-1)]
        _, output = self.execute_run(b'/bin/sh', b'-c', b'echo $PATH', environments={b'additionalEnv': {b'PATH': b':TEST_TOKEN'}})
        self.assertEqual(output[(-1)], path + b':TEST_TOKEN')

    def test_new_environment_variable(self):
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')
        _, output = self.execute_run(b'/bin/sh', b'-c', b'echo $PATH', environments={b'newEnv': {b'PATH': b'/usr/bin'}})
        self.assertEqual(output[(-1)], b'/usr/bin')

    def test_stop_run(self):
        if not os.path.exists(b'/bin/sleep'):
            self.skipTest(b'missing /bin/sleep')
        thread = _StopRunThread(1, self.runexecutor)
        thread.start()
        result, output = self.execute_run(b'/bin/sleep', b'10', expect_terminationreason=b'killed')
        thread.join()
        self.check_exitcode(result, 9, b'exit code of killed process is not 9')
        self.assertAlmostEqual(result[b'walltime'], 1, delta=0.5, msg=b'walltime is not approximately the time after which the process should have been killed')
        if b'cputime' in result:
            self.assertAlmostEqual(result[b'cputime'], trivial_run_grace_time, delta=trivial_run_grace_time, msg=b'cputime of /bin/sleep is not approximately zero')
        self.check_command_in_output(output, b'/bin/sleep 10')
        for line in output[1:]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

    def test_reduce_file_size_empty_file(self):
        with tempfile.NamedTemporaryFile() as (tmp):
            runexecutor._reduce_file_size_if_necessary(tmp.name, 0)
            self.assertEqual(os.path.getsize(tmp.name), 0)

    def test_reduce_file_size_empty_file2(self):
        with tempfile.NamedTemporaryFile() as (tmp):
            runexecutor._reduce_file_size_if_necessary(tmp.name, 500)
            self.assertEqual(os.path.getsize(tmp.name), 0)

    def test_reduce_file_size_long_line_not_truncated(self):
        with tempfile.NamedTemporaryFile(mode=b'wt') as (tmp):
            content = b'Long line ' * 500
            tmp.write(content)
            tmp.flush()
            runexecutor._reduce_file_size_if_necessary(tmp.name, 500)
            with open(tmp.name, b'rt') as (tmp2):
                self.assertMultiLineEqual(tmp2.read(), content)

    REDUCE_WARNING_MSG = b'WARNING: YOUR LOGFILE WAS TOO LONG, SOME LINES IN THE MIDDLE WERE REMOVED.'
    REDUCE_OVERHEAD = 100

    def test_reduce_file_size(self):
        with tempfile.NamedTemporaryFile(mode=b'wt') as (tmp):
            line = b'Some text\n'
            tmp.write(line * 500)
            tmp.flush()
            limit = 500
            runexecutor._reduce_file_size_if_necessary(tmp.name, limit)
            self.assertLessEqual(os.path.getsize(tmp.name), limit + self.REDUCE_OVERHEAD)
            with open(tmp.name, b'rt') as (tmp2):
                new_content = tmp2.read()
        self.assertIn(self.REDUCE_WARNING_MSG, new_content)
        self.assertTrue(new_content.startswith(line))
        self.assertTrue(new_content.endswith(line))

    def test_reduce_file_size_limit_zero(self):
        with tempfile.NamedTemporaryFile(mode=b'wt') as (tmp):
            line = b'Some text\n'
            tmp.write(line * 500)
            tmp.flush()
            runexecutor._reduce_file_size_if_necessary(tmp.name, 0)
            self.assertLessEqual(os.path.getsize(tmp.name), self.REDUCE_OVERHEAD)
            with open(tmp.name, b'rt') as (tmp2):
                new_content = tmp2.read()
        self.assertIn(self.REDUCE_WARNING_MSG, new_content)
        self.assertTrue(new_content.startswith(line))

    def test_append_crash_dump_info(self):
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')
        result, output = self.execute_run(b'/bin/sh', b'-c', b'echo "# An error report file with more information is saved as:";echo "# $(pwd)/hs_err_pid_1234.txt";echo TEST_TOKEN > hs_err_pid_1234.txt;exit 2')
        self.assertEqual(output[(-1)], b'TEST_TOKEN', b'log file misses content from crash dump file')

    def test_integration(self):
        if not os.path.exists(b'/bin/echo'):
            self.skipTest(b'missing /bin/echo')
        result, output = self.execute_run_extern(b'/bin/echo', b'TEST_TOKEN')
        self.check_exitcode_extern(result, 0, b'exit code of /bin/echo is not zero')
        self.check_result_keys(result, b'returnvalue')
        self.check_command_in_output(output, b'/bin/echo TEST_TOKEN')
        self.assertEqual(output[(-1)], b'TEST_TOKEN', b'run output misses command output')
        for line in output[1:-1]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

    def test_home_and_tmp_is_separate(self):
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')
        result, output = self.execute_run(b'/bin/sh', b'-c', b'echo $HOME $TMPDIR')
        self.check_exitcode(result, 0, b'exit code of /bin/sh is not zero')
        self.assertRegex(output[(-1)], b'/BenchExec_run_[^/]*/home .*/BenchExec_run_[^/]*/tmp', b'HOME or TMPDIR variable does not contain expected temporary directory')

    def test_temp_dirs_are_removed(self):
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')
        result, output = self.execute_run(b'/bin/sh', b'-c', b'echo $HOME $TMPDIR')
        self.check_exitcode(result, 0, b'exit code of /bin/sh is not zero')
        home_dir = output[(-1)].split(b' ')[0]
        temp_dir = output[(-1)].split(b' ')[1]
        self.assertFalse(os.path.exists(home_dir), (b'temporary home directory {} was not cleaned up').format(home_dir))
        self.assertFalse(os.path.exists(temp_dir), (b'temporary temp directory {} was not cleaned up').format(temp_dir))

    def test_home_is_writable(self):
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')
        result, output = self.execute_run(b'/bin/sh', b'-c', b'touch $HOME/TEST_FILE')
        self.check_exitcode(result, 0, (b'Failed to write to $HOME/TEST_FILE, output was\n{}').format(output))

    def test_no_cleanup_temp(self):
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')
        self.setUp(cleanup_temp_dir=False)
        result, output = self.execute_run(b'/bin/sh', b'-c', b'echo "$TMPDIR"; echo "" > "$TMPDIR/test"')
        self.check_exitcode(result, 0, b'exit code of /bin/sh is not zero')
        temp_dir = output[(-1)]
        test_file = os.path.join(temp_dir, b'test')
        subprocess.check_call([b'test', b'-f', test_file])
        self.assertEqual(b'tmp', os.path.basename(temp_dir), b'unexpected name of temp dir')
        self.assertNotEqual(b'/tmp', temp_dir, b'temp dir should not be the global temp dir')
        subprocess.check_call([b'rm', b'-r', os.path.dirname(temp_dir)])

    def test_require_cgroup_invalid(self):
        self.assertRaisesRegex(SystemExit, b'.*invalid.*', lambda : RunExecutor(additional_cgroup_subsystems=[b'invalid']))

    def test_require_cgroup_cpu(self):
        try:
            self.setUp(additional_cgroup_subsystems=[b'cpu'])
        except SystemExit as e:
            self.skipTest(e)

        if not os.path.exists(b'/bin/cat'):
            self.skipTest(b'missing /bin/cat')
        result, output = self.execute_run(b'/bin/cat', b'/proc/self/cgroup')
        self.check_exitcode(result, 0, b'exit code of /bin/cat is not zero')
        for line in output:
            if re.match(b'^[0-9]*:([^:]*,)?cpu(,[^:]*)?:/(.*/)?benchmark_.*$', line):
                return

        self.fail(b'Not in expected cgroup for subsystem cpu:\n' + (b'\n').join(output))

    def test_set_cgroup_cpu_shares(self):
        if not os.path.exists(b'/bin/echo'):
            self.skipTest(b'missing /bin/echo')
        try:
            self.setUp(additional_cgroup_subsystems=[b'cpu'])
        except SystemExit as e:
            self.skipTest(e)

        result, _ = self.execute_run(b'/bin/echo', cgroupValues={('cpu', 'shares'): 42})
        self.check_exitcode(result, 0, b'exit code of /bin/echo is not zero')

    def test_nested_runexec(self):
        if not os.path.exists(b'/bin/echo'):
            self.skipTest(b'missing /bin/echo')
        self.setUp(dir_modes={b'/': containerexecutor.DIR_READ_ONLY, 
           b'/tmp': containerexecutor.DIR_FULL_ACCESS, 
           b'/sys': containerexecutor.DIR_HIDDEN, 
           b'/sys/fs/cgroup': containerexecutor.DIR_FULL_ACCESS})
        inner_args = [
         b'--hidden-dir', b'/sys', b'--', b'/bin/echo', b'TEST_TOKEN']
        with tempfile.NamedTemporaryFile(mode=b'r', prefix=b'inner_output_', suffix=b'.log') as (inner_output_file):
            inner_cmdline = self.get_runexec_cmdline(output_filename=inner_output_file.name, *inner_args)
            outer_result, outer_output = self.execute_run(*inner_cmdline)
            inner_output = inner_output_file.read().strip().splitlines()
        logging.info(b'Outer output:\n' + (b'\n').join(outer_output))
        logging.info(b'Inner output:\n' + (b'\n').join(inner_output))
        self.check_result_keys(outer_result, b'returnvalue')
        self.check_exitcode(outer_result, 0, b'exit code of inner runexec is not zero')
        self.check_command_in_output(inner_output, b'/bin/echo TEST_TOKEN')
        self.assertEqual(inner_output[(-1)], b'TEST_TOKEN', b'run output misses command output')

    def test_starttime(self):
        if not os.path.exists(b'/bin/echo'):
            self.skipTest(b'missing /bin/echo')
        if sys.version_info[0] == 2:
            self.skipTest(b'starttime not supported on Python 2')
        before = util.read_local_time()
        result, _ = self.execute_run(b'/bin/echo')
        after = util.read_local_time()
        self.check_result_keys(result)
        run_starttime = result[b'starttime']
        self.assertIsNotNone(run_starttime.tzinfo, b'start time is not a local time')
        self.assertLessEqual(before, run_starttime)
        self.assertLessEqual(run_starttime, after)


class TestRunExecutorWithContainer(TestRunExecutor):

    def setUp(self, *args, **kwargs):
        try:
            container.execute_in_namespace(lambda : 0)
        except OSError as e:
            self.skipTest((b'Namespaces not supported: {}').format(os.strerror(e.errno)))

        dir_modes = kwargs.pop(b'dir_modes', {b'/': containerexecutor.DIR_READ_ONLY, 
           b'/home': containerexecutor.DIR_HIDDEN, 
           b'/tmp': containerexecutor.DIR_HIDDEN})
        self.runexecutor = RunExecutor(use_namespaces=True, dir_modes=dir_modes, *args, **kwargs)

    def get_runexec_cmdline(self, *args, **kwargs):
        return [
         python,
         runexec,
         b'--container',
         b'--read-only-dir',
         b'/',
         b'--hidden-dir',
         b'/home',
         b'--hidden-dir',
         b'/tmp',
         b'--dir',
         b'/tmp',
         b'--output',
         kwargs[b'output_filename']] + list(args)

    def execute_run(self, *args, **kwargs):
        return super(TestRunExecutorWithContainer, self).execute_run(workingDir=b'/tmp', *args, **kwargs)

    def test_home_and_tmp_is_separate(self):
        self.skipTest(b'not relevant in container')

    def test_temp_dirs_are_removed(self):
        self.skipTest(b'not relevant in container')

    def test_no_cleanup_temp(self):
        self.skipTest(b'not relevant in container')

    def check_result_files(self, shell_cmd, result_files_patterns, expected_result_files):
        output_dir = tempfile.mkdtemp(b'', b'output_')
        try:
            result, output = self.execute_run(b'/bin/sh', b'-c', shell_cmd, output_dir=output_dir, result_files_patterns=result_files_patterns)
            self.assertEqual(result[b'exitcode'].value, 0, (b'exit code of {} is not zero,\nresult was {!r},\noutput was\n{}').format((b' ').join(shell_cmd), result, (b'\n').join(output)))
            result_files = []
            for root, unused_dirs, files in os.walk(output_dir):
                for file in files:
                    result_files.append(os.path.relpath(os.path.join(root, file), output_dir))

            expected_result_files.sort()
            result_files.sort()
            self.assertListEqual(result_files, expected_result_files, (b'\nList of retrieved result files differs from expected list,\nresult was {!r},\noutput was\n{}').format(result, (b'\n').join(output)))
        finally:
            shutil.rmtree(output_dir, ignore_errors=True)

    def test_result_file_simple(self):
        self.check_result_files(b'echo TEST_TOKEN > TEST_FILE', [b'.'], [b'TEST_FILE'])

    def test_result_file_recursive(self):
        self.check_result_files(b'mkdir TEST_DIR; echo TEST_TOKEN > TEST_DIR/TEST_FILE', [
         b'.'], [
         b'TEST_DIR/TEST_FILE'])

    def test_result_file_multiple(self):
        self.check_result_files(b'echo TEST_TOKEN > TEST_FILE; echo TEST_TOKEN > TEST_FILE2', [
         b'.'], [
         b'TEST_FILE', b'TEST_FILE2'])

    def test_result_file_symlink(self):
        self.check_result_files(b'echo TEST_TOKEN > TEST_FILE; ln -s TEST_FILE TEST_LINK', [
         b'.'], [
         b'TEST_FILE'])

    def test_result_file_no_match(self):
        self.check_result_files(b'echo TEST_TOKEN > TEST_FILE', [b'NO_MATCH'], [])

    def test_result_file_no_pattern(self):
        self.check_result_files(b'echo TEST_TOKEN > TEST_FILE', [], [])

    def test_result_file_empty_pattern(self):
        self.assertRaises(ValueError, lambda : self.check_result_files(b'echo TEST_TOKEN > TEST_FILE', [b''], []))

    def test_result_file_partial_match(self):
        self.check_result_files(b'echo TEST_TOKEN > TEST_FILE; mkdir TEST_DIR; echo TEST_TOKEN > TEST_DIR/TEST_FILE', [
         b'TEST_DIR'], [
         b'TEST_DIR/TEST_FILE'])

    def test_result_file_multiple_patterns(self):
        self.check_result_files(b'echo TEST_TOKEN > TEST_FILE; echo TEST_TOKEN > TEST_FILE2; mkdir TEST_DIR; echo TEST_TOKEN > TEST_DIR/TEST_FILE; ', [
         b'TEST_FILE', b'TEST_DIR/TEST_FILE'], [
         b'TEST_FILE', b'TEST_DIR/TEST_FILE'])

    def test_result_file_wildcard(self):
        self.check_result_files(b'echo TEST_TOKEN > TEST_FILE; echo TEST_TOKEN > TEST_FILE2; echo TEST_TOKEN > TEST_NOFILE; ', [
         b'TEST_FILE*'], [
         b'TEST_FILE', b'TEST_FILE2'])

    def test_result_file_absolute_pattern(self):
        self.check_result_files(b'echo TEST_TOKEN > TEST_FILE', [b'/'], [b'tmp/TEST_FILE'])

    def test_result_file_absolute_and_pattern(self):
        self.check_result_files(b'echo TEST_TOKEN > TEST_FILE; mkdir TEST_DIR; echo TEST_TOKEN > TEST_DIR/TEST_FILE', [
         b'TEST_FILE', b'/tmp/TEST_DIR'], [
         b'tmp/TEST_FILE', b'tmp/TEST_DIR/TEST_FILE'])

    def test_result_file_relative_traversal(self):
        self.check_result_files(b'echo TEST_TOKEN > TEST_FILE', [b'foo/../TEST_FILE'], [b'TEST_FILE'])

    def test_result_file_illegal_relative_traversal(self):
        self.assertRaises(ValueError, lambda : self.check_result_files(b'echo TEST_TOKEN > TEST_FILE', [b'foo/../../bar'], []))

    def test_result_file_recursive_pattern(self):
        if not util.maybe_recursive_iglob == glob.iglob:
            self.skipTest(b'missing recursive glob.iglob')
        self.check_result_files(b'mkdir -p TEST_DIR/TEST_DIR; echo TEST_TOKEN > TEST_FILE.txt; echo TEST_TOKEN > TEST_DIR/TEST_FILE.txt; echo TEST_TOKEN > TEST_DIR/TEST_DIR/TEST_FILE.txt; ', [
         b'**/*.txt'], [
         b'TEST_FILE.txt',
         b'TEST_DIR/TEST_FILE.txt',
         b'TEST_DIR/TEST_DIR/TEST_FILE.txt'])

    def test_file_count_limit(self):
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')
        self.setUp(container_tmpfs=False)
        filehierarchylimit._CHECK_INTERVAL_SECONDS = 0.1
        result, output = self.execute_run(b'/bin/sh', b'-c', b'for i in $(seq 1 10000); do touch $i; done', files_count_limit=100, result_files_patterns=None, expect_terminationreason=b'files-count')
        self.check_exitcode(result, 9, b'exit code of killed process is not 15')
        for line in output[1:]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

        return

    def test_file_size_limit(self):
        if not os.path.exists(b'/bin/sh'):
            self.skipTest(b'missing /bin/sh')
        self.setUp(container_tmpfs=False)
        filehierarchylimit._CHECK_INTERVAL_SECONDS = 0.1
        result, output = self.execute_run(b'/bin/sh', b'-c', b'for i in $(seq 1 100000); do echo $i >> TEST_FILE; done', files_size_limit=100, result_files_patterns=None, expect_terminationreason=b'files-size')
        self.check_exitcode(result, 9, b'exit code of killed process is not 15')
        for line in output[1:]:
            self.assertRegex(line, b'^-*$', b'unexpected text in run output')

        return

    def test_path_with_space(self):
        temp_dir = tempfile.mkdtemp(prefix=b'BenchExec test')
        try:
            self.setUp(dir_modes={b'/': containerexecutor.DIR_READ_ONLY, 
               b'/home': containerexecutor.DIR_HIDDEN, 
               b'/tmp': containerexecutor.DIR_HIDDEN, 
               temp_dir: containerexecutor.DIR_FULL_ACCESS})
            temp_file = os.path.join(temp_dir, b'TEST_FILE')
            result, output = self.execute_run(b'/bin/sh', b'-c', (b"echo TEST_TOKEN > '{}'").format(temp_file))
            self.check_result_keys(result)
            self.check_exitcode(result, 0, b'exit code of process is not 0')
            self.assertTrue(os.path.exists(temp_file), (b"File '{}' not created, output was:{}\n").format(temp_file, (b'\n').join(output)))
            with open(temp_file, b'r') as (f):
                self.assertEqual(f.read().strip(), b'TEST_TOKEN')
        finally:
            shutil.rmtree(temp_dir)

    def test_uptime_with_lxcfs(self):
        if not os.path.exists(b'/var/lib/lxcfs/proc'):
            self.skipTest(b'missing lxcfs')
        result, output = self.execute_run(b'cat', b'/proc/uptime')
        self.check_result_keys(result)
        self.check_exitcode(result, 0, b'exit code for reading uptime is not zero')
        uptime = float(output[(-1)].split(b' ')[0])
        self.assertLessEqual(uptime, 10, b'Uptime %ss unexpectedly high in container' % uptime)

    def test_uptime_without_lxcfs(self):
        if not os.path.exists(b'/var/lib/lxcfs/proc'):
            self.skipTest(b'missing lxcfs')
        self.setUp(container_system_config=False)
        result, output = self.execute_run(b'cat', b'/proc/uptime')
        self.check_result_keys(result)
        self.check_exitcode(result, 0, b'exit code for reading uptime is not zero')
        uptime = float(output[(-1)].split(b' ')[0])
        self.assertGreaterEqual(uptime, 10, b'Uptime %ss unexpectedly low in container' % uptime)


class _StopRunThread(threading.Thread):

    def __init__(self, delay, runexecutor):
        super(_StopRunThread, self).__init__()
        self.daemon = True
        self.delay = delay
        self.runexecutor = runexecutor

    def run(self):
        time.sleep(self.delay)
        self.runexecutor.stop()


class TestRunExecutorUnits(unittest.TestCase):
    """unit tests for parts of RunExecutor"""

    def test_get_debug_output_with_error_report_and_invalid_utf8(self):
        invalid_utf8 = b'\xff'
        with tempfile.NamedTemporaryFile(mode=b'w+b', delete=False) as (report_file):
            with tempfile.NamedTemporaryFile(mode=b'w+b') as (output):
                output_content = b'Dummy output\n# An error report file with more information is saved as:\n# {}\nMore output\n'
                output_content = output_content.format(report_file.name).encode()
                report_content = b'Report output\nMore lines'
                output_content += invalid_utf8
                report_content += invalid_utf8
                output.write(output_content)
                output.flush()
                output.seek(0)
                report_file.write(report_content)
                report_file.flush()
                runexecutor._get_debug_output_after_crash(output.name, b'')
                self.assertFalse(os.path.exists(report_file.name))
                self.assertEqual(output.read(), output_content + report_content)