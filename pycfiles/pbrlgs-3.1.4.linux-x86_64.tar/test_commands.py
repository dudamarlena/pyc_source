# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/tests/test_commands.py
# Compiled at: 2017-12-04 07:19:32
from testtools import content
from pbr.tests import base

class TestCommands(base.BaseTestCase):

    def test_custom_build_py_command(self):
        """Test custom build_py command.

        Test that a custom subclass of the build_py command runs when listed in
        the commands [global] option, rather than the normal build command.
        """
        stdout, stderr, return_code = self.run_setup('build_py')
        self.addDetail('stdout', content.text_content(stdout))
        self.addDetail('stderr', content.text_content(stderr))
        self.assertIn('Running custom build_py command.', stdout)
        self.assertEqual(0, return_code)

    def test_custom_deb_version_py_command(self):
        """Test custom deb_version command."""
        stdout, stderr, return_code = self.run_setup('deb_version')
        self.addDetail('stdout', content.text_content(stdout))
        self.addDetail('stderr', content.text_content(stderr))
        self.assertIn('Extracting deb version', stdout)
        self.assertEqual(0, return_code)

    def test_custom_rpm_version_py_command(self):
        """Test custom rpm_version command."""
        stdout, stderr, return_code = self.run_setup('rpm_version')
        self.addDetail('stdout', content.text_content(stdout))
        self.addDetail('stderr', content.text_content(stderr))
        self.assertIn('Extracting rpm version', stdout)
        self.assertEqual(0, return_code)

    def test_freeze_command(self):
        """Test that freeze output is sorted in a case-insensitive manner."""
        stdout, stderr, return_code = self.run_pbr('freeze')
        self.assertEqual(0, return_code)
        pkgs = []
        for l in stdout.split('\n'):
            pkgs.append(l.split('==')[0].lower())

        pkgs_sort = sorted(pkgs[:])
        self.assertEqual(pkgs_sort, pkgs)