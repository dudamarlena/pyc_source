# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/management/commands/index.py
# Compiled at: 2020-02-11 04:03:56
import optparse
from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
     optparse.make_option('--full', action='store_true', dest='rebuild', default=False, help='Rebuild the database index'),)
    help = 'Creates a search index of review requests'
    requires_model_validation = True

    def handle(self, *args, **options):
        if options['rebuild']:
            call_command('rebuild_index', interactive=False)
        else:
            call_command('update_index')