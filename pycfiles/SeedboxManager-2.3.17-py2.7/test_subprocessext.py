# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/tasks/test_subprocessext.py
# Compiled at: 2015-06-14 13:30:57
from __future__ import absolute_import
from distutils.sysconfig import get_python_lib
import os, subprocess, testtools
from seedbox.tasks import subprocessext
from seedbox.tests import test

class SubprocessExtTest(test.ConfiguredBaseTestCase):

    def setUp(self):
        super(SubprocessExtTest, self).setUp()
        self.CONF.set_override('stdout_dir', self.CONF.tasks_synclog.stdout_dir, group='tasks_synclog')
        self.CONF.set_override('stderr_dir', self.CONF.tasks_synclog.stderr_dir, group='tasks_synclog')
        if not os.path.exists(self.CONF.tasks_synclog.stdout_dir):
            os.mkdir(self.CONF.tasks_synclog.stdout_dir)
        if not os.path.exists(self.CONF.tasks_synclog.stderr_dir):
            os.mkdir(self.CONF.tasks_synclog.stderr_dir)
        self.py_lib = os.path.abspath(os.path.join(get_python_lib(), '..'))

    def test_short_single_cmd(self):
        self.CONF.set_override('stdout_verbose', True, group='tasks_synclog')
        self.CONF.set_override('stderr_verbose', True, group='tasks_synclog')
        cmd = [
         'ls']
        subprocessext.ProcessLogging.execute(cmd)
        self.assertTrue(True)

    def test_long_single_cmd(self):
        cmd = [
         'ls', '-laR', self.py_lib]
        subprocessext.ProcessLogging.execute(cmd)
        self.assertTrue(True)

    def test_short_multi_cmd(self):
        for cmd in [['ls'], ['ls', '--help'], ['tail', '--help'],
         [
          'ps', '--help'], ['mv', '--help']]:
            subprocessext.ProcessLogging.execute(cmd)
            self.assertTrue(True)

    def test_long_multi_cmd(self):
        for cmd in [['ls', '-laR', self.py_lib],
         [
          'ls', '-laR', os.path.expanduser('~')]]:
            subprocessext.ProcessLogging.execute(cmd)
            self.assertTrue(True)

    def test_bad_cmd(self):
        cmd = ['ls', 'some_unknown_or_missing_file']
        with testtools.ExpectedException(subprocess.CalledProcessError):
            subprocessext.ProcessLogging.execute(cmd)

    def test_multi_good_bad_cmd(self):
        for cmd in [['ls', 'some_unknown_or_missing_file'], ['ls', '--help'],
         [
          'ls', 'another_unknown_or_missing_file'],
         [
          'ps', '--help'],
         [
          'ls', 'and_another_unknown_or_missing_file']]:
            if '--help' in cmd:
                subprocessext.ProcessLogging.execute(cmd)
                self.assertTrue(True)
            else:
                with testtools.ExpectedException(subprocess.CalledProcessError):
                    subprocessext.ProcessLogging.execute(cmd)