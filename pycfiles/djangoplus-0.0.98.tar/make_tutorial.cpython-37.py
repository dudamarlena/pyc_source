# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/opt/.virtualenvs/djangoplus/lib/python3.7/site-packages/djangoplus/docs/management/commands/make_tutorial.py
# Compiled at: 2018-08-05 18:47:44
# Size of source mod 2**32: 780 bytes
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--continue', action='store_true', dest='continue', default=False, help='Will not create a new project. The existing one will be used.')

    def handle(self, *args, **options):
        fromlist = [
         settings.PROJECT_NAME, 'tutorial', 'AppTutorial']
        module = __import__(('{}.tutorial'.format(settings.PROJECT_NAME)), fromlist=fromlist)
        tutorial = module.AppTutorial(settings.BASE_DIR)
        create_project = not options.pop('continue', False)
        tutorial.start(create_project)