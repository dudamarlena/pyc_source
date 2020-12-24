# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/staticfiles/management/commands/findstatic.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import os
from django.contrib.staticfiles import finders
from django.core.management.base import LabelCommand
from django.utils.encoding import force_text

class Command(LabelCommand):
    help = b'Finds the absolute paths for the given static file(s).'
    label = b'staticfile'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(b'--first', action=b'store_false', dest=b'all', default=True, help=b'Only return the first match for each static file.')

    def handle_label(self, path, **options):
        verbosity = options[b'verbosity']
        result = finders.find(path, all=options[b'all'])
        path = force_text(path)
        if verbosity >= 2:
            searched_locations = b'\nLooking in the following locations:\n  %s' % (b'\n  ').join(force_text(location) for location in finders.searched_locations)
        else:
            searched_locations = b''
        if result:
            if not isinstance(result, (list, tuple)):
                result = [
                 result]
            result = (force_text(os.path.realpath(path)) for path in result)
            if verbosity >= 1:
                file_list = (b'\n  ').join(result)
                return b"Found '%s' here:\n  %s%s" % (
                 path, file_list, searched_locations)
            return (b'\n').join(result)
        else:
            message = [
             b"No matching file found for '%s'." % path]
            if verbosity >= 2:
                message.append(searched_locations)
            if verbosity >= 1:
                self.stderr.write((b'\n').join(message))