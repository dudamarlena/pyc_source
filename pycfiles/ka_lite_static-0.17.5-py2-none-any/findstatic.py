# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/staticfiles/management/commands/findstatic.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import os
from optparse import make_option
from django.core.management.base import LabelCommand
from django.utils.encoding import smart_text
from django.contrib.staticfiles import finders

class Command(LabelCommand):
    help = b'Finds the absolute paths for the given static file(s).'
    args = b'[file ...]'
    label = b'static file'
    option_list = LabelCommand.option_list + (
     make_option(b'--first', action=b'store_false', dest=b'all', default=True, help=b'Only return the first match for each static file.'),)

    def handle_label(self, path, **options):
        verbosity = int(options.get(b'verbosity', 1))
        result = finders.find(path, all=options[b'all'])
        path = smart_text(path)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [
                 result]
            output = (b'\n  ').join(smart_text(os.path.realpath(path)) for path in result)
            self.stdout.write(b"Found '%s' here:\n  %s" % (path, output))
        elif verbosity >= 1:
            self.stderr.write(b"No matching file found for '%s'." % path)