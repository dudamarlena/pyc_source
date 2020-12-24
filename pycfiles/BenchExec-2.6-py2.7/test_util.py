# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/test_util.py
# Compiled at: 2020-05-07 05:52:35
from __future__ import absolute_import, division, print_function, unicode_literals
import datetime, sys, unittest
from benchexec.util import ProcessExitCode
import tempfile, os, stat
from benchexec import util
sys.dont_write_bytecode = True

class TestParse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.longMessage = True
        cls.maxDiff = None
        return

    def assertEqualNumberAndUnit(self, value, number, unit):
        self.assertEqual(util.split_number_and_unit(value), (number, unit))

    def test_split_number_and_unit(self):
        self.assertEqualNumberAndUnit(b'1', 1, b'')
        self.assertEqualNumberAndUnit(b'1s', 1, b's')
        self.assertEqualNumberAndUnit(b'  1  s  ', 1, b's')
        self.assertEqualNumberAndUnit(b'-1s', -1, b's')
        self.assertEqualNumberAndUnit(b'1abc', 1, b'abc')
        self.assertEqualNumberAndUnit(b'1  abc  ', 1, b'abc')
        self.assertRaises(ValueError, util.split_number_and_unit, b'')
        self.assertRaises(ValueError, util.split_number_and_unit, b'abc')
        self.assertRaises(ValueError, util.split_number_and_unit, b's')
        self.assertRaises(ValueError, util.split_number_and_unit, b'a1a')
        try:
            self.assertEqualNumberAndUnit(b'- 1', -1, b'')
        except ValueError:
            pass

    def test_parse_memory_value(self):
        self.assertEqual(util.parse_memory_value(b'1'), 1)
        self.assertEqual(util.parse_memory_value(b'1B'), 1)
        self.assertEqual(util.parse_memory_value(b'1kB'), 1000)
        self.assertEqual(util.parse_memory_value(b'1MB'), 1000000)
        self.assertEqual(util.parse_memory_value(b'1GB'), 1000000000)
        self.assertEqual(util.parse_memory_value(b'1TB'), 1000000000000)

    def test_parse_timespan_value(self):
        self.assertEqual(util.parse_timespan_value(b'1'), 1)
        self.assertEqual(util.parse_timespan_value(b'1s'), 1)
        self.assertEqual(util.parse_timespan_value(b'1min'), 60)
        self.assertEqual(util.parse_timespan_value(b'1h'), 3600)
        self.assertEqual(util.parse_timespan_value(b'1d'), 86400)


class TestProcessExitCode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.longMessage = True
        cls.maxDiff = None
        return

    def ProcessExitCode_with_value(self, value):
        return ProcessExitCode(raw=value << 8, value=value, signal=None)

    def ProcessExitCode_with_signal(self, signal):
        return ProcessExitCode(raw=signal, value=None, signal=signal)

    def test_boolness(self):
        self.assertFalse(self.ProcessExitCode_with_value(0))
        self.assertTrue(self.ProcessExitCode_with_value(1))
        self.assertTrue(self.ProcessExitCode_with_signal(1))

    def test_value(self):
        self.assertEqual(self.ProcessExitCode_with_value(0).value, 0)
        self.assertEqual(self.ProcessExitCode_with_value(1).value, 1)
        self.assertEqual(ProcessExitCode.from_raw(0).value, 0)
        self.assertEqual(ProcessExitCode.from_raw(256).value, 1)
        self.assertIsNone(self.ProcessExitCode_with_signal(1).value)
        self.assertIsNone(ProcessExitCode.from_raw(1).value)

    def test_signal(self):
        self.assertEqual(self.ProcessExitCode_with_signal(1).signal, 1)
        self.assertEqual(ProcessExitCode.from_raw(1).signal, 1)
        self.assertIsNone(self.ProcessExitCode_with_value(0).signal)
        self.assertIsNone(self.ProcessExitCode_with_value(1).signal)
        self.assertIsNone(ProcessExitCode.from_raw(0).signal)
        self.assertIsNone(ProcessExitCode.from_raw(256).signal)


class TestRmtree(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.longMessage = True
        cls.maxDiff = None
        return

    def setUp(self):
        self.base_dir = tempfile.mkdtemp(prefix=b'BenchExec_test_util_rmtree')

    def test_writable_file(self):
        util.write_file(b'', self.base_dir, b'tempfile')
        util.rmtree(self.base_dir)
        self.assertFalse(os.path.exists(self.base_dir), b'Failed to remove directory with file')

    def test_writable_dir(self):
        os.mkdir(os.path.join(self.base_dir, b'tempdir'))
        util.rmtree(self.base_dir)
        self.assertFalse(os.path.exists(self.base_dir), b'Failed to remove directory with child directory')

    def test_nonwritable_file(self):
        temp_file = os.path.join(self.base_dir, b'tempfile')
        util.write_file(b'', temp_file)
        os.chmod(temp_file, 0)
        util.rmtree(self.base_dir)
        self.assertFalse(os.path.exists(self.base_dir), b'Failed to remove directory with non-writable file')

    def create_and_delete_directory(self, mode):
        tempdir = os.path.join(self.base_dir, b'tempdir')
        os.mkdir(tempdir)
        util.write_file(b'', tempdir, b'tempfile')
        os.chmod(tempdir, mode)
        util.rmtree(self.base_dir)
        self.assertFalse(os.path.exists(self.base_dir), b'Failed to remove directory')

    def test_nonwritable_dir(self):
        self.create_and_delete_directory(stat.S_IRUSR | stat.S_IXUSR)

    def test_nonexecutable_dir(self):
        self.create_and_delete_directory(stat.S_IRUSR | stat.S_IWUSR)

    def test_nonreadable_dir(self):
        self.create_and_delete_directory(stat.S_IWUSR | stat.S_IXUSR)

    def test_dir_without_any_permissions(self):
        self.create_and_delete_directory(0)

    def test_read_local_time(self):
        """Test on Python 3.6+ that the fallback for older Pythons does the same."""
        try:
            time = datetime.datetime.now().astimezone()
        except (ValueError, TypeError):
            self.skipTest(b'datetime.datetime.now().astimezone() not supported')

        time2 = util.read_local_time()
        self.assertLess(time2 - time, datetime.timedelta(seconds=1))