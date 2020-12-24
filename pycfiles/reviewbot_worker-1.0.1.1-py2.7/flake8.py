# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/tools/flake8.py
# Compiled at: 2018-07-31 04:26:56
"""Review Bot tool to run flake8."""
from __future__ import unicode_literals
from reviewbot.tools import Tool
from reviewbot.utils.process import execute, is_exe_in_path

class Flake8Tool(Tool):
    """Review Bot tool to run flake8."""
    name = b'flake8'
    version = b'1.0'
    description = b'Checks Python code for style and programming errors.'
    timeout = 30
    options = [
     {b'name': b'max_line_length', 
        b'field_type': b'django.forms.IntegerField', 
        b'default': 79, 
        b'field_options': {b'label': b'Maximum Line Length', 
                           b'help_text': b'The maximum line length to allow.', 
                           b'required': True}},
     {b'name': b'ignore', 
        b'field_type': b'django.forms.CharField', 
        b'default': b'', 
        b'field_options': {b'label': b'Ignore', 
                           b'help_text': b'A comma-separated list of errors and warnings to ignore. This will be passed to the --ignore command line argument (e.g. E4,W).', 
                           b'required': False}}]

    def check_dependencies(self):
        """Verify that the tool's dependencies are installed.

        Returns:
            bool:
            True if all dependencies for the tool are satisfied. If this
            returns False, the worker will not be listed for this Tool's queue,
            and a warning will be logged.
        """
        return is_exe_in_path(b'flake8')

    def handle_file(self, f, settings):
        """Perform a review of a single file.

        Args:
            f (reviewbot.processing.review.File):
                The file to process.

            settings (dict):
                Tool-specific settings.
        """
        if not f.dest_file.lower().endswith(b'.py'):
            return
        path = f.get_patched_file_path()
        if not path:
            return
        output = execute([
         b'flake8',
         b'--exit-zero',
         b'--max-line-length=%s' % settings[b'max_line_length'],
         b'--ignore=%s' % settings[b'ignore'],
         path], split_lines=True)
        for line in output:
            try:
                line = line[len(path) + 1:]
                line_num, column, message = line.split(b':', 2)
                f.comment(message.strip(), int(line_num))
            except Exception:
                pass