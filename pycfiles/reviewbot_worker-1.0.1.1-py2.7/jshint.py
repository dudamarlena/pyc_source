# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/tools/jshint.py
# Compiled at: 2018-07-31 04:26:56
from __future__ import unicode_literals
import re
from reviewbot.tools import Tool
from reviewbot.utils.filesystem import make_tempfile
from reviewbot.utils.process import execute, is_exe_in_path

class JSHintTool(Tool):
    """Review Bot tool to run jshint."""
    name = b'JSHint'
    version = b'1.0'
    description = b'Checks JavaScript code for style errors and potential problems using JSHint, a JavaScript Code Quality Tool.'
    timeout = 30
    options = [
     {b'name': b'verbose', 
        b'field_type': b'django.forms.BooleanField', 
        b'default': False, 
        b'field_options': {b'label': b'Verbose', 
                           b'help_text': b'Includes message codes in the JSHint output.', 
                           b'required': False}},
     {b'name': b'extra_ext_checks', 
        b'field_type': b'django.forms.CharField', 
        b'default': b'', 
        b'field_options': {b'label': b'Extra File Extensions', 
                           b'help_text': b'A comma-separated list of extra file extensions to check (only .js is included by default).', 
                           b'required': False}},
     {b'name': b'extract_js_from_html', 
        b'field_type': b'django.forms.ChoiceField', 
        b'field_options': {b'label': b'Extract JavaScript from HTML', 
                           b'help_text': b'Whether JSHint should extract JavaScript from HTML files. If set to "auto", it will only try extracting JavaScript if the file looks like an HTML file.', 
                           b'choices': (
                                      ('auto', 'auto'),
                                      ('always', 'always'),
                                      ('never', 'never')), 
                           b'initial': b'never', 
                           b'required': False}},
     {b'name': b'config', 
        b'field_type': b'djblets.db.fields.JSONFormField', 
        b'default': b'', 
        b'field_options': {b'label': b'Configuration', 
                           b'help_text': b'JSON specifying which JSHint options to turn on or off. (This is equivalent to the contents of a .jshintrc file.)', 
                           b'required': False}, 
        b'widget': {b'type': b'django.forms.Textarea', 
                    b'attrs': {b'cols': 70, 
                               b'rows': 10}}}]
    REGEX = re.compile(b'\\S+: line (?P<line_num>\\d+), col (?P<col>\\d+),(?P<msg>.+)')

    def check_dependencies(self):
        """Verify the tool's dependencies are installed.

        Returns:
            bool:
            True if all dependencies for the tool are satisfied. If this
            returns False, the worker will not listen for this Tool's queue,
            and a warning will be logged.
        """
        return is_exe_in_path(b'jshint')

    def handle_files(self, files, settings):
        """Perform a review of all files.

        Args:
            files (list of reviewbot.processing.review.File):
                The files to process.

            settings (dict):
                Tool-specific settings.
        """
        self.file_exts = None
        if settings[b'extra_ext_checks']:
            self.file_exts = tuple(settings[b'extra_ext_checks'].split(b','))
        self.config_file = None
        if settings[b'config']:
            self.config_file = make_tempfile(content=settings[b'config'])
        super(JSHintTool, self).handle_files(files, settings)
        return

    def handle_file(self, f, settings):
        """Perform a review of a single file.

        Args:
            f (reviewbot.processing.review.File):
                The file to process.

            settings (dict):
                Tool-specific settings.
        """
        if not (f.dest_file.endswith(b'.js') or self.file_exts and f.dest_file.endswith(self.file_exts)):
            return
        path = f.get_patched_file_path()
        if not path:
            return
        cmd = [b'jshint', b'--extract=%s' % settings[b'extract_js_from_html']]
        if settings[b'verbose']:
            cmd.append(b'--verbose')
        if self.config_file:
            cmd.append(b'--config=%s' % self.config_file)
        cmd.append(path)
        output = execute(cmd, split_lines=True, ignore_errors=True)
        for line in output:
            m = re.match(self.REGEX, line)
            if m:
                f.comment(b'Col: %s\n%s' % (m.group(b'col'), m.group(b'msg')), int(m.group(b'line_num')))