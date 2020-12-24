# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev-light/application/backend/apps/ohm2_handlers_light/management/commands/ohm2_handlers_test_command.py
# Compiled at: 2017-07-20 17:22:27
# Size of source mod 2**32: 1027 bytes
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from ohm2_handlers_light import utils as h_utils
from ohm2_handlers_light import models as handlers_models
from ohm2_handlers_light.definitions import RunException

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """
                be = h_utils.db_create(handlers_models.BaseError, last_update = timezone.now())

                print(be.identity)

                """
        from Crypto import Random
        from Crypto.Cipher import AES
        import base64
        key_16, iv_16 = h_utils.random_string(16), base64.b64encode(Random.new().read(AES.block_size))
        print(iv_16)
        message = h_utils.random_string(16)
        encrypted = h_utils.encrypt_aes_cfb(key_16, iv_16, message)
        print(encrypted.hex())
        print(message, h_utils.decrypt_aes_cfb(key_16, iv_16, encrypted))