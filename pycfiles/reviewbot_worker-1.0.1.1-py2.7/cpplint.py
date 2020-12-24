# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/tools/cpplint.py
# Compiled at: 2018-07-31 04:26:56
from __future__ import unicode_literals
import re
from reviewbot.tools import Tool
from reviewbot.utils.process import execute, is_exe_in_path

class CPPLintTool(Tool):
    """Review Bot tool to run cpplint."""
    name = b'cpplint'
    version = b'1.0'
    description = b"Checks code for style errors using Google's cpplint tool."
    timeout = 30
    options = [
     {b'name': b'verbosity', 
        b'field_type': b'django.forms.IntegerField', 
        b'default': 1, 
        b'min_value': 1, 
        b'max_value': 5, 
        b'field_options': {b'label': b'Verbosity level for CPP Lint', 
                           b'help_text': b'Which level of messages should be displayed. 1=All, 5=Few.', 
                           b'required': True}},
     {b'name': b'excluded_checks', 
        b'field_type': b'django.forms.CharField', 
        b'default': b'', 
        b'field_options': {b'label': b'Tests to exclude', 
                           b'help_text': b'Comma-separated list of tests to exclude (run cpplint.py --filter= to see all possible choices).', 
                           b'required': False}}]

    def check_dependencies(self):
        """Verify the tool's dependencies are installed.

        Returns:
            bool:
            True if all dependencies for the tool are satisfied. If this
            returns False, the worker will not listen for this Tool's queue,
            and a warning will be logged.
        """
        return is_exe_in_path(b'cpplint')

    def handle_file(self, f, settings):
        """Perform a review of a single file.

        Args:
            f (reviewbot.processing.review.File):
                The file to process.

            settings (dict):
                Tool-specific settings.
        """
        if not (f.dest_file.lower().endswith(b'.cpp') or f.dest_file.lower().endswith(b'.h')):
            return
        path = f.get_patched_file_path()
        if not path:
            return
        if settings[b'excluded_checks']:
            output = execute([
             b'cpplint',
             b'--verbose=%s' % settings[b'verbosity'],
             b'--filter=%s' % settings[b'excluded_checks'],
             path], split_lines=True, ignore_errors=True)
        else:
            output = execute([
             b'cpplint',
             b'--verbose=%s' % self.settings[b'verbosity'],
             path], split_lines=True, ignore_errors=True)
        for line in output:
            matching_obj = re.findall(b'(\\S+:)(\\d+:)(.+?\\[)(.+?\\])(.+)', line)
            linenumber = 0
            freetext = b''
            category = b''
            verbosity = b''
            for match in matching_obj:
                linenumber = int(match[1][:-1])
                freetext = match[2][:-1].strip()
                category = match[3][:-1].strip()
                verbosity = match[4][2:-1].strip()
                f.comment(b'%s.\n\nError Group: %s\nVerbosity Level: %s' % (
                 freetext, category, verbosity), linenumber)