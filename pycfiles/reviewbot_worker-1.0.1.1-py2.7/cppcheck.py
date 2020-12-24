# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/tools/cppcheck.py
# Compiled at: 2018-07-31 04:26:56
from __future__ import unicode_literals
from reviewbot.tools import Tool
from reviewbot.utils.process import execute, is_exe_in_path

class CPPCheckTool(Tool):
    """Review Bot tool to run cppcheck."""
    name = b'Cppcheck'
    version = b'1.0'
    description = b'Checks code for errors using Cppcheck, a tool for static C/C++ code analysis.'
    timeout = 30
    options = [
     {b'name': b'style_checks_enabled', 
        b'field_type': b'django.forms.BooleanField', 
        b'default': True, 
        b'field_options': {b'label': b'Enable standard style checks', 
                           b'help_text': b'Enable the standard style checks, including most warning, style, and performance checks.', 
                           b'required': False}},
     {b'name': b'all_checks_enabled', 
        b'field_type': b'django.forms.BooleanField', 
        b'default': False, 
        b'field_options': {b'label': b'Enable ALL error checks', 
                           b'help_text': b'Enable all the error checks. This is likely to include many false positives.', 
                           b'required': False}},
     {b'name': b'force_language', 
        b'field_type': b'django.forms.ChoiceField', 
        b'field_options': {b'label': b'Use language', 
                           b'help_text': b'Force cppcheck to use a specific language.', 
                           b'choices': (
                                      ('', 'auto-detect'),
                                      ('c', 'C'),
                                      ('c++', 'C++')), 
                           b'initial': b'', 
                           b'required': False}}]

    def check_dependencies(self):
        """Verify the tool's dependencies are installed.

        Returns:
            bool:
            True if all dependencies for the tool are satisfied. If this
            returns False, the worker will not listen for this Tool's queue,
            and a warning will be logged.
        """
        return is_exe_in_path(b'cppcheck')

    def handle_file(self, f, settings):
        """Perform a review of a single file.

        Args:
            f (reviewbot.processing.review.File):
                The file to process.

            settings (dict):
                Tool-specific settings.
        """
        if not (f.dest_file.lower().endswith(b'.cpp') or f.dest_file.lower().endswith(b'.h') or f.dest_file.lower().endswith(b'.c')):
            return
        path = f.get_patched_file_path()
        if not path:
            return
        enabled_checks = []
        if settings[b'style_checks_enabled']:
            enabled_checks.append(b'style')
        if settings[b'all_checks_enabled']:
            enabled_checks.append(b'all')
        enable_settings = b'%s' % (b',').join(map(str, enabled_checks))
        cppcheck_args = [
         b'cppcheck',
         b'--template="{file}::{line}::{severity}::{id}::{message}"',
         b'--enable=%s' % enable_settings]
        lang = settings[b'force_language'].strip()
        if lang:
            cppcheck_args.append(b'--language=%s' % lang)
        cppcheck_args.append(path)
        output = execute(cppcheck_args, split_lines=True, ingore_errors=True)
        for line in output:
            parsed = line.split(b'::')
            if len(parsed) == 5:
                if parsed[1]:
                    linenumber = int(parsed[1])
                else:
                    linenumber = 0
                category = parsed[2]
                sub_category = parsed[3]
                freetext = parsed[4][:-1]
                if category == b'error':
                    f.comment(b'%s.\n\nCategory: %s\nSub Category: %s' % (
                     freetext, category, sub_category), linenumber, issue=True)
                else:
                    f.comment(b'%s.\n\nCategory: %s\nSub Category: %s' % (
                     freetext, category, sub_category), linenumber, issue=False)