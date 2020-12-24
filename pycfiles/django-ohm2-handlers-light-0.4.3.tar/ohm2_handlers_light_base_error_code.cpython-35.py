# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev-light/application/backend/apps/ohm2_handlers_light/management/commands/ohm2_handlers_light_base_error_code.py
# Compiled at: 2017-05-26 17:42:49
# Size of source mod 2**32: 413 bytes
from django.core.management.base import BaseCommand, CommandError
from ohm2_handlers_light import utils as h_utils
from subprocess import call
import os

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write('{0}'.format(h_utils.get_base_error_code()))