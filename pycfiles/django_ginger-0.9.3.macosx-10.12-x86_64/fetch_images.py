# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/management/commands/fetch_images.py
# Compiled at: 2015-02-12 18:07:09
from django.conf import settings
import os, optparse
from ginger.extras.google_images import GoogleImage
from django.core.management import BaseCommand, CommandError

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
     optparse.make_option('-s', '--size', action='store', dest='size'),
     optparse.make_option('-f', '--file-type', type='choice', choices=[
      'jpg', 'png', 'svg'], default='jpg'),
     optparse.make_option('-u', '--unsafe', action='store_true'),
     optparse.make_option('-p', '--prefix', default='image'),
     optparse.make_option('-c', '--count', default=10, type='int'))

    def handle(self, query, dest=None, *args, **options):
        if dest is None:
            dest = ''
        gi = GoogleImage(dest, options['prefix'])
        results = gi.search(query, options['count'], safe=not options['unsafe'], file_type=options['file_type'])
        verbosity = int(options['verbosity'])
        for img in results:
            msg = 'Downloaded %s \n' % img
            if verbosity:
                self.stdout.write(msg)

        return