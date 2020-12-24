# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/test_cgroups.py
# Compiled at: 2019-11-28 13:06:29
from __future__ import absolute_import, division, print_function, unicode_literals
import logging, os, subprocess, sys, unittest
sys.dont_write_bytecode = True
from benchexec import check_cgroups
try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, b'wb')

python = b'python2' if sys.version_info[0] == 2 else b'python3'

class TestCheckCgroups(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.longMessage = True
        cls.maxDiff = None
        logging.disable(logging.CRITICAL)
        return

    def execute_run_extern(self, *args, **kwargs):
        try:
            return subprocess.check_output(args=([
             python, b'-m', b'benchexec.check_cgroups'] + list(args)), stderr=subprocess.STDOUT, **kwargs).decode()
        except subprocess.CalledProcessError as e:
            if e.returncode != 1:
                print(e.output.decode())
                raise e

    def test_extern_command(self):
        self.execute_run_extern()

    def test_simple(self):
        try:
            check_cgroups.main([b'--no-thread'])
        except SystemExit as e:
            self.skipTest(e)

    def test_threaded(self):
        try:
            check_cgroups.main([])
        except SystemExit as e:
            self.skipTest(e)

    def test_thread_result_is_returned(self):
        """
        Test that an error raised by check_cgroup_availability is correctly
        re-raised in the main thread by replacing this function temporarily.
        """
        tmp = check_cgroups.check_cgroup_availability
        try:
            check_cgroups.check_cgroup_availability = lambda wait: exit(1)
            with self.assertRaises(SystemExit):
                check_cgroups.main([])
        finally:
            check_cgroups.check_cgroup_availability = tmp