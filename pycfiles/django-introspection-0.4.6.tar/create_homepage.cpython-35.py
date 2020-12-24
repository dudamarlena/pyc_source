# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo52/mogo/alapage/management/commands/create_homepage.py
# Compiled at: 2017-06-14 09:33:36
# Size of source mod 2**32: 603 bytes
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from alapage.models import Page

class Command(BaseCommand):
    help = 'Creates a homepage'

    def handle(self, *args, **options):
        content = ''
        home_exists = Page.objects.filter(url='/').exists()
        if not home_exists:
            Page.objects.create(url='/', title='Home', content=content)
            print('Homepage created')
        else:
            print('The homepage already exists with root url')