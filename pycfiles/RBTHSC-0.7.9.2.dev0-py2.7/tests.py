# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\utils\tests.py
# Compiled at: 2017-04-19 05:14:04
from __future__ import unicode_literals
import os, re, shutil, sys
from rbtools.utils import aliases, checks, filesystem, process
from rbtools.utils.testbase import RBTestBase

class UtilitiesTest(RBTestBase):
    """Tests for rbtools.api units.

    Any new modules created under rbtools/api should be tested here.
    """

    def test_check_install(self):
        """Testing 'check_install' method."""
        self.assertTrue(checks.check_install([sys.executable, b' --version']))
        self.assertFalse(checks.check_install([self.gen_uuid()]))

    def test_make_tempfile(self):
        """Testing 'make_tempfile' method."""
        fname = filesystem.make_tempfile()
        self.assertTrue(os.path.isfile(fname))
        self.assertEqual(os.stat(fname).st_uid, os.geteuid())
        self.assertTrue(os.access(fname, os.R_OK | os.W_OK))

    def test_make_empty_files(self):
        """Testing 'make_empty_files' method."""
        tmpdir = filesystem.make_tempdir()
        self.assertTrue(os.path.isdir(tmpdir))
        filesystem.cleanup_tempfiles()
        fname = os.path.join(tmpdir, b'file')
        filesystem.make_empty_files([fname])
        self.assertTrue(os.path.isdir(tmpdir))
        self.assertTrue(os.path.isfile(fname))
        self.assertEqual(os.stat(fname).st_uid, os.geteuid())
        self.assertTrue(os.access(fname, os.R_OK | os.W_OK))
        shutil.rmtree(tmpdir, ignore_errors=True)

    def test_execute(self):
        """Testing 'execute' method."""
        self.assertTrue(re.match(b'.*?%d.%d.%d' % sys.version_info[:3], process.execute([sys.executable, b'-V'])))

    def test_die(self):
        """Testing 'die' method."""
        self.assertRaises(SystemExit, process.die)

    def test_is_valid_version(self):
        """Testing 'is_valid_version' method."""
        self.assertTrue(checks.is_valid_version((1, 0, 0), (1, 0, 0)))
        self.assertTrue(checks.is_valid_version((1, 1, 0), (1, 0, 0)))
        self.assertTrue(checks.is_valid_version((1, 0, 1), (1, 0, 0)))
        self.assertTrue(checks.is_valid_version((1, 1, 0), (1, 1, 0)))
        self.assertTrue(checks.is_valid_version((1, 1, 1), (1, 1, 0)))
        self.assertTrue(checks.is_valid_version((1, 1, 1), (1, 1, 1)))
        self.assertFalse(checks.is_valid_version((0, 9, 9), (1, 0, 0)))
        self.assertFalse(checks.is_valid_version((1, 0, 9), (1, 1, 0)))
        self.assertFalse(checks.is_valid_version((1, 1, 0), (1, 1, 1)))


class AliasTest(RBTestBase):
    """Tests for parameter substitution in rbtools aliases."""

    def _replace_arguments(self, cmd, args):
        """Convenience method to return a list instead of generator.

        This allows us to compare with self.assertEqual to another list.
        """
        return list(aliases.replace_arguments(cmd, args))

    def test_alias_substitution_basic(self):
        """Testing variable substitution in rbtools aliases"""
        self.assertEqual(self._replace_arguments(b'$1', [b'HEAD']), [
         b'HEAD'])

    def test_alias_subtitution_multiple(self):
        """Testing variable substitution where multiple variables appear"""
        self.assertEqual(self._replace_arguments(b'$1..$2', [b'a', b'b']), [
         b'a..b'])

    def test_alias_substitution_blank(self):
        """Testing variable substitution where the argument isn't supplied"""
        self.assertEqual(self._replace_arguments(b'rbt post $1', []), [
         b'rbt', b'post', b''])

    def test_alias_substitution_append(self):
        """Testing variable substitution where no variables are supplied"""
        self.assertEqual(self._replace_arguments(b'echo', [b'a', b'b', b'c']), [
         b'echo', b'a', b'b', b'c'])

    def test_alias_dont_substitute_alphabetic_variables(self):
        """Testing variable substitution with alphabetic variables"""
        self.assertEqual(self._replace_arguments(b'$1 $test', [b'f']), [
         b'f', b'$test'])

    def test_alias_substitution_star(self):
        """Testing variable substitution with the $* variable"""
        self.assertEqual(self._replace_arguments(b'$*', [b'a', b'b', b'c']), [
         b'a', b'b', b'c'])

    def test_alias_substitution_star_whitespace(self):
        """Testing $* variable substitution with whitespace-containing args"""
        self.assertEqual(self._replace_arguments(b'$*', [b'a', b'b', b'c d e']), [
         b'a', b'b', b'c d e'])

    def test_alias_substitution_bad_quotes(self):
        """Testing alias substitution with bad quotes."""
        self.assertRaises(ValueError, lambda : self._replace_arguments(b'"$1 $2\\"', []))

    def test_alias_substition_unescaped_quotes(self):
        """Testing alias substitution with a slash at the end of the string"""
        self.assertEqual(self._replace_arguments(b'"$1 \\\\"', [b'a']), [b'a \\'])