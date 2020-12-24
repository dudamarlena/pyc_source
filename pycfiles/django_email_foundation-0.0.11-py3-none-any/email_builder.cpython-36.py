# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/farpi/Workspace/cesc/django-email-foundation/django_email_foundation/management/commands/email_builder.py
# Compiled at: 2019-03-15 10:07:07
# Size of source mod 2**32: 844 bytes
from typing import List
from django.core.management import BaseCommand
from django_email_foundation.api import DjangoEmailFoundation

class Command(BaseCommand):
    help = 'Run a service for watch and compile the email templates'

    def handle(self, *args, **options):
        engine = DjangoEmailFoundation()
        errors = engine.perform_checks()
        if errors:
            self._show_errors(errors)
            return
        self.stdout.write(self.style.SUCCESS('Oh, yes! Punchi, punchi! Lets go!'))
        engine = DjangoEmailFoundation()
        engine.run_watch()

    def _show_errors(self, errors: List[str]):
        self.stdout.write(self.style.ERROR('Oops! Something went wrong...'))
        for error in errors:
            self.stdout.write(self.style.ERROR('  - {}'.format(error)))

        self.stdout.write('\n')