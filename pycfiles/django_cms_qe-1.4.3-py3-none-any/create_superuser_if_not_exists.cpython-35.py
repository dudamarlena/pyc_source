# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/management/commands/create_superuser_if_not_exists.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 749 bytes
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = get_user_model().objects.filter(is_superuser=True).first()
        if user:
            self.stdout.write("The superuser '{}' already exists.".format(user.username))
        else:
            password = 'admin'
            user = get_user_model().objects.create_superuser('admin', 'admin@example.com', password)
            self.stdout.write('A new superuser with the following data was created:\n                login:    {}\n                email:    {}\n                password: {}'.format(user.username, user.email, password))