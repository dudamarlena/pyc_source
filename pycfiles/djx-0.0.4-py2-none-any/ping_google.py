# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/sitemaps/management/commands/ping_google.py
# Compiled at: 2019-02-14 00:35:17
from django.contrib.sitemaps import ping_google
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Ping Google with an updated sitemap, pass optional url of sitemap'

    def add_arguments(self, parser):
        parser.add_argument('sitemap_url', nargs='?', default=None)
        return

    def handle(self, *args, **options):
        ping_google(sitemap_url=options['sitemap_url'])