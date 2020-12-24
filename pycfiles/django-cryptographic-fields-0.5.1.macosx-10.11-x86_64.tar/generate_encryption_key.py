# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dana/.virtualenvs/django-cryptographic-fields/lib/python2.7/site-packages/cryptographic_fields/management/commands/generate_encryption_key.py
# Compiled at: 2016-02-04 23:28:53
from django.core.management.base import BaseCommand
import cryptography.fernet

class Command(BaseCommand):
    help = 'Generates a new Fernet encryption key'

    def handle(self, *args, **options):
        key = cryptography.fernet.Fernet.generate_key()
        self.stdout.write(key)