# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/lifestyle/lifestyle/alapage/management/commands/create_page.py
# Compiled at: 2017-05-29 08:22:34
# Size of source mod 2**32: 718 bytes
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from alapage.models import Page

class Command(BaseCommand):
    help = 'Creates a page'

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='+', type=str)
        parser.add_argument('url', nargs='+', type=str)

    def handle(self, *args, **options):
        name = options['name'][0]
        url = options['url'][0]
        exists = Page.objects.filter(url=url).exists()
        if not exists:
            Page.objects.create(url=url, title=name)
            print('Page ' + name + ' created')
        else:
            print('The page already exists at ' + url)