# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/management/commands/list_users.py
# Compiled at: 2019-10-23 19:45:21
# Size of source mod 2**32: 528 bytes
from django.core.management.base import BaseCommand
from djconnectwise.models import Member

class Command(BaseCommand):
    help = 'List active, full-license ConnectWise members.'

    def handle(self, *args, **options):
        for member in Member.objects.filter(inactive=False, license_class='F'):
            self.stdout.write('{:15} {:20} {:43}'.format(member.identifier, member.__str__(), member.office_email))