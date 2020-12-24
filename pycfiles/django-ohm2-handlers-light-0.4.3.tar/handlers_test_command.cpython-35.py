# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/v0.3.0/development/website/handlers/management/commands/handlers_test_command.py
# Compiled at: 2016-05-05 20:14:46
# Size of source mod 2**32: 583 bytes
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from handlers import utils as h_utils
from handlers import models as handlers_models

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
                be = h_utils.db_create(handlers_models.BaseError, last_update = timezone.now())

                print(be.identity)

                """
        image = h_utils.get_local_image('/Users/tonra/Downloads/Lg_logo-6.jpg')
        print(image.size, image.name)