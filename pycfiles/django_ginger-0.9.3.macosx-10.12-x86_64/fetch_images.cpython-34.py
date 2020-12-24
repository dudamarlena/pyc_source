# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/management/commands/fetch_images.py
# Compiled at: 2015-11-20 22:30:15
# Size of source mod 2**32: 1397 bytes
from ginger.extras.google_images import GoogleImage
from django.core.management import BaseCommand

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('query')
        parser.add_argument('--dest', default=None)
        parser.add_argument('-s', '--size', action='store', dest='size')
        parser.add_argument('-f', '--file-type', type=str, choices=[
         'jpg', 'png', 'svg'], default='jpg')
        parser.add_argument('-u', '--unsafe', action='store_true')
        parser.add_argument('-p', '--prefix', default='image')
        parser.add_argument('-c', '--count', default=10, type=int)

    def handle(self, **options):
        query = options['query']
        dest = options['dest']
        gi = GoogleImage(dest, options['prefix'])
        results = gi.search(query, options['count'], safe=not options['unsafe'], file_type=options['file_type'])
        verbosity = int(options['verbosity'])
        for img in results:
            msg = 'Downloaded %s \n' % img
            if verbosity:
                self.stdout.write(msg)
                continue