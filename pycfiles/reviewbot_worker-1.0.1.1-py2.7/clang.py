# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/tools/clang.py
# Compiled at: 2018-07-31 04:26:56
from __future__ import unicode_literals
import plistlib, shlex
from reviewbot.tools import RepositoryTool
from reviewbot.utils.filesystem import make_tempfile
from reviewbot.utils.process import execute, is_exe_in_path

class ClangTool(RepositoryTool):
    """Review Bot tool to run clang --analyze."""
    name = b'Clang Static Analyzer'
    version = b'1.0'
    description = b'Checks code using clang --analyze.'
    timeout = 30
    options = [
     {b'name': b'cmdline_args', 
        b'field_type': b'django.forms.CharField', 
        b'default': b'', 
        b'field_options': {b'label': b'Clang command-line arguments', 
                           b'help_text': b'Any additional arguments to include on the command-line when invoking clang --analyze. Used primarily to set include paths.', 
                           b'required': False}}]

    def check_dependencies(self):
        """Verify the tool's dependencies are installed.

        Returns:
            bool:
            True if all dependencies for the tool are satisfied. If this
            returns False, the worker will not listen for this Tool's queue,
            and a warning will be logged.
        """
        return is_exe_in_path(b'clang')

    def handle_file(self, f, settings):
        """Perform a review of a single file.

        Args:
            f (reviewbot.processing.review.File):
                The file to process.

            settings (dict):
                Tool-specific settings.
        """
        filename = f.dest_file.lower()
        if not filename.endswith(('.c', '.cpp', '.cxx', '.m', '.mm')):
            return
        path = f.get_patched_file_path()
        if not path:
            return
        additional_args = []
        configured_args = settings.get(b'cmdline_args')
        if configured_args:
            additional_args = shlex.split(configured_args)
        outfile = make_tempfile()
        command = [
         b'clang', b'-S', b'--analyze']
        if filename.endswith(b'.m'):
            command.append(b'-ObjC')
        else:
            if filename.endswith(b'.mm'):
                command.append(b'-ObjC++')
            command += additional_args
            command += [path, b'-Xanalyzer', b'-analyzer-output=plist', b'-o',
             outfile]
            self.output = execute(command, ignore_errors=True)
            results = plistlib.readPlist(outfile)
            for diagnostic in results[b'diagnostics']:
                file_index = diagnostic[b'location'][b'file']
                filename = results[b'files'][file_index]
                if filename != f.dest_file:
                    continue
                line, num_lines = self._find_linenums(diagnostic)
                f.comment(diagnostic[b'description'], line, num_lines)

    def _find_linenums(self, diagnostic):
        """Find and return the given line numbers.

        Args:
            diagnostic (dict):
                The diagnostic to find the line numbers for.

        Returns:
            tuple of int:
            A 2-tuple, consisting of the line number and the number of lines
            covered by the given diagnostic.
        """
        for path_node in diagnostic.get(b'path', []):
            if path_node[b'kind'] == b'event' and b'ranges' in path_node:
                line_range = path_node[b'ranges'][0]
                first_line = line_range[0][b'line']
                last_line = line_range[1][b'line']
                return (
                 first_line, last_line - first_line + 1)

        first_line = diagnostic[b'location'][b'line']
        return (first_line, 1)