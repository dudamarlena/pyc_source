# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/tools/pyflakes.py
# Compiled at: 2018-07-31 04:26:56
from __future__ import unicode_literals
from reviewbot.tools import Tool
from reviewbot.utils.process import execute, is_exe_in_path

class PyflakesTool(Tool):
    """Review Bot tool to run pyflakes."""
    name = b'Pyflakes'
    version = b'1.0'
    description = b'Checks Python code for errors using Pyflakes.'
    timeout = 30

    def check_dependencies(self):
        """Verify the tool's dependencies are installed.

        Returns:
            bool:
            True if all dependencies for the tool are satisfied. If this
            returns False, the worker will not listen for this Tool's queue,
            and a warning will be logged.
        """
        return is_exe_in_path(b'pyflakes')

    def handle_file(self, f, settings):
        """Perform a review of a single file.

        Args:
            f (reviewbot.processing.review.File):
                The file to process.

            settings (dict):
                Tool-specific settings.
        """
        if not f.dest_file.endswith(b'.py'):
            return
        path = f.get_patched_file_path()
        if not path:
            return
        output = execute([
         b'pyflakes',
         path], split_lines=True, ignore_errors=True)
        for line in output:
            parsed = line.split(b':', 2)
            lnum = int(parsed[1])
            msg = parsed[2]
            f.comment(b'%s' % (msg,), lnum)