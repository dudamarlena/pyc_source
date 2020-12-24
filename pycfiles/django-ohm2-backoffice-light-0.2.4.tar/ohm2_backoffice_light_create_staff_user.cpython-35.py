# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/clients/ohm2/entwicklung/ohm2-dev-light/webapp/backend/apps/ohm2_backoffice_light/management/commands/ohm2_backoffice_light_create_staff_user.py
# Compiled at: 2017-12-28 20:17:14
# Size of source mod 2**32: 593 bytes
from django.core.management.base import BaseCommand, CommandError
from ohm2_handlers_light import utils as h_utils
from ohm2_backoffice_light import utils as ohm2_backoffice_light_utils
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
        ohm2_backoffice_light_utils.create_staff_user(username, email, password)