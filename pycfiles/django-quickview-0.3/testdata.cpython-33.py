# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Dev\python\django-quickview\docs\examplesite\friendslist\management\commands\testdata.py
# Compiled at: 2013-02-26 03:19:13
# Size of source mod 2**32: 2060 bytes
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from friendslist.models import *

class Command(BaseCommand):
    args = ''
    help = 'Creates a lot of test data.'

    def handle(self, *args, **options):
        self.stdout.write('Adding user ...')
        for username in ('thomas', 'cecilie'):
            user = User.objects.create_user(username, '%s@weholt.org' % username, 'test')
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()

        friendslist = ('Thomas Weholt', 'Cecilie Weholt', 'Emrik Weholt', 'Tuva Weholt',
                       'Tore Olsen', 'Turid Olsen', 'Lena Gjertsen', 'Kjetil Gjertsen',
                       'Kevin Olsen', 'Kenneth Olsen', 'Ivar SkovSkov', 'Vivian SkovSkov',
                       'Roger Kristiansen', 'Inge Norheim', 'Kristin Norheim', 'Kristin Weholt',
                       'Karianne Weholt', 'Arild Weholt', 'Anne Weholt', 'Jimmy Olsen',
                       'Linda Olsen', 'Marthine Gjertsen', 'Aaron Gjertsen', 'Katta Olsen',
                       'Camilla Olsen', 'Ronny OverGata', 'Hanne OverGata', 'Sander Hansen',
                       'Mathias Hansen', 'Snore Hansen')
        for friend in friendslist:
            firstname, lastname = friend.split(' ')
            Friend.objects.create(name=friend, email='%s@%s.com' % (firstname, lastname), address='Hollywood Bld. 1911', city='Los Angeles', zip_code='02-666', country='America', phone='555 - 42 - 666')

        self.stdout.write('Successfully created initial data.')