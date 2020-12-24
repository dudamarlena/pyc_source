# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/todd/github/restructuredtext-lint/restructuredtext_lint/test/test.py
# Compiled at: 2019-01-06 05:01:34
from __future__ import absolute_import
import os, subprocess, sys, textwrap
from unittest import TestCase
import restructuredtext_lint
__dir__ = os.path.dirname(os.path.abspath(__file__))
valid_rst = os.path.join(__dir__, 'test_files', 'valid.rst')
warning_rst = os.path.join(__dir__, 'test_files', 'second_short_heading.rst')
dir_rst = os.path.join(__dir__, 'test_files', 'dir')
invalid_rst = os.path.join(__dir__, 'test_files', 'invalid.rst')
rst_lint_path = os.path.join(__dir__, os.pardir, 'cli.py')

class TestRestructuredtextLint(TestCase):

    def _load_file(self, filepath):
        """Load a file into memory"""
        f = open(filepath)
        file = f.read()
        f.close()
        return file

    def _lint_file(self, *args, **kwargs):
        """Lint the file and preserve any errors"""
        return restructuredtext_lint.lint(*args, **kwargs)

    def test_passes_valid_rst(self):
        """A valid reStructuredText file will not raise any errors"""
        content = self._load_file(valid_rst)
        errors = self._lint_file(content)
        self.assertEqual(errors, [])

    def test_raises_on_invalid_rst(self):
        """An invalid reStructuredText file when linted raises errors"""
        content = self._load_file(invalid_rst)
        actual_errors = self._lint_file(content, invalid_rst)
        self.assertEqual(len(actual_errors), 1)
        self.assertEqual(actual_errors[0].line, 2)
        self.assertEqual(actual_errors[0].level, 2)
        self.assertEqual(actual_errors[0].type, 'WARNING')
        self.assertEqual(actual_errors[0].source, invalid_rst)
        self.assertEqual(actual_errors[0].message, 'Title underline too short.')

    def test_encoding_utf8(self):
        """A document with utf-8 characters is valid."""
        filepath = os.path.join(__dir__, 'test_files', 'utf8.rst')
        errors = restructuredtext_lint.lint_file(filepath, encoding='utf-8')
        self.assertEqual(errors, [])

    def test_second_heading_short_line_number(self):
        """A document with a short second heading raises errors that include a line number

        This is a regression test for https://github.com/twolfson/restructuredtext-lint/issues/5
        """
        filepath = os.path.join(__dir__, 'test_files', 'second_short_heading.rst')
        errors = restructuredtext_lint.lint_file(filepath)
        self.assertEqual(errors[0].line, 6)
        self.assertEqual(errors[0].source, filepath)

    def test_invalid_target(self):
        """A document with an invalid target name raises an error

        This is a regression test for https://github.com/twolfson/restructuredtext-lint/issues/6
        """
        filepath = os.path.join(__dir__, 'test_files', 'invalid_target.rst')
        errors = restructuredtext_lint.lint_file(filepath)
        self.assertIn('Unknown target name', errors[0].message)

    def test_invalid_line_mismatch(self):
        """A document with an overline/underline mismatch raises an error

        This is a regression test for https://github.com/twolfson/restructuredtext-lint/issues/7
        """
        filepath = os.path.join(__dir__, 'test_files', 'invalid_line_mismatch.rst')
        errors = restructuredtext_lint.lint_file(filepath)
        self.assertIn('Title overline & underline mismatch', errors[0].message)

    def test_invalid_link(self):
        """A document with a bad link raises an error

        This is a regression test for https://github.com/twolfson/restructuredtext-lint/issues/12
        """
        filepath = os.path.join(__dir__, 'test_files', 'invalid_link.rst')
        errors = restructuredtext_lint.lint_file(filepath)
        self.assertIn('Anonymous hyperlink mismatch: 1 references but 0 targets.', errors[0].message)
        self.assertIn('Hyperlink target "hello" is not referenced.', errors[1].message)

    def test_rst_prolog_basic(self):
        """A document using substitutions from an `rst-prolog` has no errors"""
        rst_prolog = textwrap.dedent('\n        .. |World| replace:: Moon\n        ')
        content = textwrap.dedent('\n        Hello\n        =====\n        |World|\n        ')
        errors = restructuredtext_lint.lint(content)
        self.assertEqual(len(errors), 1)
        self.assertIn('Undefined substitution referenced: "World"', errors[0].message)
        errors = restructuredtext_lint.lint(content, rst_prolog=rst_prolog)
        self.assertEqual(len(errors), 0)

    def test_rst_prolog_line_offset(self):
        """A document with errors using an `rst-prolog` offsets our error lines"""
        rst_prolog = textwrap.dedent('\n        .. |World| replace:: Moon\n        ')
        content = textwrap.dedent('\n        Hello\n        ==\n        |World|\n        ')
        errors = restructuredtext_lint.lint(content, rst_prolog=rst_prolog)
        self.assertEqual(len(errors), 1)
        self.assertIn('Possible title underline, too short for the title', errors[0].message)
        self.assertEqual(errors[0].line, 3)


class TestRestructuredtextLintCLI(TestCase):
    """ Tests for 'rst-lint' CLI command """

    def test_rst_lint_filepaths_not_given(self):
        """The `rst-lint` command is available and prints error if no filepath was given."""
        with self.assertRaises(subprocess.CalledProcessError) as (e):
            subprocess.check_output((sys.executable, rst_lint_path), stderr=subprocess.STDOUT)
        output = str(e.exception.output)
        self.assertIn('arguments', output)

    def test_rst_lint_correct_file(self):
        """The `rst-lint` command prints nothing if rst file is correct."""
        raw_output = subprocess.check_output((sys.executable, rst_lint_path, valid_rst), universal_newlines=True)
        output = str(raw_output)
        self.assertEqual(output, '')

    def test_rst_lint_folder(self):
        """The `rst-lint` command should print errors for files inside folders."""
        with self.assertRaises(subprocess.CalledProcessError) as (e):
            subprocess.check_output((sys.executable, rst_lint_path, dir_rst), universal_newlines=True)
        output = str(e.exception.output)
        self.assertEqual(output.count('WARNING'), 1)

    def test_rst_lint_many_files(self):
        """The `rst-lint` command accepts many rst file paths and prints respective information for each of them."""
        with self.assertRaises(subprocess.CalledProcessError) as (e):
            subprocess.check_output((sys.executable, rst_lint_path, valid_rst, invalid_rst), universal_newlines=True)
        output = str(e.exception.output)
        self.assertEqual(e.exception.returncode, 2)
        self.assertEqual(output.count('\n'), 1, output)
        self.assertIn('WARNING', output)

    def test_level_fail(self):
        """Confirm low --level threshold fails file with warnings only"""
        with self.assertRaises(subprocess.CalledProcessError) as (e):
            subprocess.check_output((sys.executable, rst_lint_path, '--level', 'warning', warning_rst), universal_newlines=True)
        output = str(e.exception.output)
        self.assertEqual(output.count('\n'), 2, output)
        self.assertEqual(output.count('WARNING'), 2, output)
        self.assertEqual(e.exception.returncode, 2)

    def test_level_high(self):
        """Confirm high --level threshold accepts file with warnings only"""
        raw_output = subprocess.check_output((sys.executable, rst_lint_path, '--level', 'error', warning_rst), universal_newlines=True)
        output = str(raw_output)
        self.assertEqual(output, '')