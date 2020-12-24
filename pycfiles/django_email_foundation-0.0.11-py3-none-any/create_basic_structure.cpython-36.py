# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/farpi/Workspace/cesc/django-email-foundation/django_email_foundation/management/commands/create_basic_structure.py
# Compiled at: 2019-03-25 06:27:07
# Size of source mod 2**32: 758 bytes
from django.core.management import BaseCommand
from django_email_foundation.api import DjangoEmailFoundation, Checks

class Command(BaseCommand):
    help = 'Create the necessary folders inside the template path and it add a basic layout.'

    def handle(self, *args, **options):
        checks = Checks()
        if not checks.templates_source_path():
            self.stdout.write(self.style.ERROR('You must to define the templates source path.'))
            return
        else:
            self.stdout.write('Creating folders...')
            engine = DjangoEmailFoundation()
            error = engine.create_basic_structure()
            if error:
                self.stderr.write(self.style.ERROR(error))
            else:
                self.stdout.write(self.style.SUCCESS('Done!'))