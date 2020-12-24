# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/sitemaps/management/commands/ping_google.py
# Compiled at: 2018-07-11 18:15:31
from django.core.management.base import BaseCommand
from django.contrib.sitemaps import ping_google

class Command(BaseCommand):
    help = 'Ping Google with an updated sitemap, pass optional url of sitemap'

    def execute(self, *args, **options):
        if len(args) == 1:
            sitemap_url = args[0]
        else:
            sitemap_url = None
        ping_google(sitemap_url=sitemap_url)
        return