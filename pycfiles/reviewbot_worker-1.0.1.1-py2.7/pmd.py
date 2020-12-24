# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/tools/pmd.py
# Compiled at: 2018-07-31 04:26:56
from __future__ import unicode_literals
import csv, logging
from os.path import splitext
from reviewbot.config import config
from reviewbot.tools import Tool
from reviewbot.utils.filesystem import make_tempfile
from reviewbot.utils.process import execute, is_exe_in_path

class PMDTool(Tool):
    """Review Bot tool to run PMD."""
    name = b'PMD'
    version = b'1.0'
    description = b'Checks code for errors using the PMD source code checker.'
    timeout = 90
    options = [
     {b'name': b'rulesets', 
        b'field_type': b'django.forms.CharField', 
        b'default': b'', 
        b'field_options': {b'label': b'Rulesets', 
                           b'help_text': b'A comma-separated list of rulesets to apply or an XML configuration starting with "<?xml"', 
                           b'required': True}, 
        b'widget': {b'type': b'django.forms.Textarea', 
                    b'attrs': {b'cols': 80, 
                               b'rows': 10}}},
     {b'name': b'file_ext', 
        b'field_type': b'django.forms.CharField', 
        b'default': b'java', 
        b'field_options': {b'label': b'Scan files', 
                           b'help_text': b'Comma-separated list of file extensions to scan. Leave it empty to check any file.', 
                           b'required': False}}]

    def check_dependencies(self):
        """Verify the tool's dependencies are installed.

        Returns:
            bool:
            True if all dependencies for the tool are satisfied. If this
            returns False, the worker will not listen for this Tool's queue,
            and a warning will be logged.
        """
        pmd_path = config[b'pmd_path']
        return pmd_path and is_exe_in_path(pmd_path)

    def handle_file(self, f, settings):
        """Perform a review of a single file.

        Args:
            f (reviewbot.processing.review.File):
                The file to process.

            settings (dict):
                Tool-specific settings.
        """
        file_ext = settings[b'file_ext'].strip()
        if file_ext:
            ext = splitext(f.dest_file)[1][1:]
            if ext.lower() not in file_ext.split(b','):
                return
        path = f.get_patched_file_path()
        if not path:
            return
        rulesets = settings[b'rulesets']
        if rulesets.startswith(b'<?xml'):
            rulesets = make_tempfile(rulesets)
        outfile = make_tempfile()
        execute([
         config[b'pmd_path'],
         b'pmd',
         b'-d', path,
         b'-R', rulesets,
         b'-f', b'csv',
         b'-r', outfile], ignore_errors=True)
        with open(outfile) as (result):
            reader = csv.DictReader(result)
            for row in reader:
                try:
                    f.comment(row[b'Description'], int(row[b'Line']))
                except Exception as e:
                    logging.error(b'Cannot parse line "%s": %s', row, e)