# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/tools/checkstyle.py
# Compiled at: 2018-07-31 04:26:56
"""Review Bot tool to run checkstyle."""
from __future__ import unicode_literals
import logging
from xml.etree import ElementTree
from reviewbot.config import config
from reviewbot.tools import Tool
from reviewbot.utils.filesystem import make_tempfile
from reviewbot.utils.process import execute, is_exe_in_path

class CheckstyleTool(Tool):
    """Review Bot tool to run checkstyle."""
    name = b'checkstyle'
    version = b'1.0'
    description = b'Checks code for errors using checkstyle.'
    timeout = 90
    options = [
     {b'name': b'config', 
        b'field_type': b'django.forms.CharField', 
        b'default': b'', 
        b'field_options': {b'label': b'Configuration xml', 
                           b'help_text': b'Content of configuration xml. See: http://checkstyle.sourceforge.net/config.html', 
                           b'required': True}, 
        b'widget': {b'type': b'django.forms.Textarea', 
                    b'attrs': {b'cols': 80, 
                               b'rows': 10}}}]

    def check_dependencies(self):
        """Verify the tool's dependencies are installed.

        Returns:
            bool:
            True if all dependencies for the tool are satisfied. If this
            returns False, the worker will not listen for this Tool's queue,
            and a warning will be logged.
        """
        checkstyle_path = config[b'checkstyle_path']
        return checkstyle_path and is_exe_in_path(checkstyle_path) and is_exe_in_path(b'java')

    def handle_file(self, f, settings):
        """Perform a review of a single file.

        Args:
            f (reviewbot.processing.review.File):
                The file to process.

            settings (dict):
                Tool-specific settings.
        """
        if not f.dest_file.lower().endswith(b'.java'):
            return
        path = f.get_patched_file_path()
        if not path:
            return
        cfgXml = make_tempfile(settings[b'config'])
        outfile = make_tempfile()
        execute([
         b'java',
         b'-jar',
         config[b'checkstyle_path'],
         b'-c', cfgXml,
         b'-f', b'xml',
         b'-o', outfile,
         path], ignore_errors=True)
        try:
            root = ElementTree.parse(outfile).getroot()
            for row in root.iter(b'error'):
                f.comment(row.get(b'message'), int(row.get(b'line')))

        except Exception as e:
            logging.error(b'Cannot parse xml file: %s', e)