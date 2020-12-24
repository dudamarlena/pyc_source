# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/accounts/management/commands/accounts_create_superuser.py
# Compiled at: 2017-01-24 22:19:05
# Size of source mod 2**32: 570 bytes
from django.core.management.base import BaseCommand, CommandError
from ohm2_handlers import utils as h_utils
from ohm2_handlers.accounts import utils as accounts_utils
import os

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username')
        parser.add_argument('-e', '--email')
        parser.add_argument('-p', '--password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        user = accounts_utils.create_superuser(username, email, password)