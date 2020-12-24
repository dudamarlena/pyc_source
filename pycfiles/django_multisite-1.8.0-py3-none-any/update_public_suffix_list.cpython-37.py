# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jordi/vcs/django-multisite/multisite/management/commands/update_public_suffix_list.py
# Compiled at: 2019-05-02 13:25:00
# Size of source mod 2**32: 1068 bytes
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
import logging, os, tempfile
from django.conf import settings
from django.core.management.base import BaseCommand
import tldextract

class Command(BaseCommand):

    def handle(self, **options):
        self.setup_logging(verbosity=(options.get('verbosity', 1)))
        filename = getattr(settings, 'MULTISITE_PUBLIC_SUFFIX_LIST_CACHE', os.path.join(tempfile.gettempdir(), 'multisite_tld.dat'))
        self.log('Updating {filename}'.format(filename=filename))
        extract = tldextract.TLDExtract(cache_file=filename)
        extract.update(fetch_now=True)
        self.log('Done.')

    def setup_logging(self, verbosity):
        self.verbosity = int(verbosity)
        self.logger = logging.getLogger('tldextract')
        if self.verbosity < 2:
            self.logger.setLevel(logging.CRITICAL)

    def log(self, msg):
        self.logger.info(msg)