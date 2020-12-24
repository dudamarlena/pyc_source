# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/admin/Desktop/package_env/django_confirm_phone/phonenumber_confirmation/managers.py
# Compiled at: 2020-04-03 13:29:23
# Size of source mod 2**32: 613 bytes
from django.db import models

class PhoneNumberManager(models.Manager):

    def add_phone_number(self, user, phone, primary=False, confirm=False):
        phone_number, created = self.get_or_create(user=user, phone=phone,
          primary=primary)
        if created:
            if confirm:
                phone.send(phone_number, confirm)
        return phone_number

    def get_primary(self, user):
        try:
            return self.get(user=user, primary=True)
        except self.model.DoesNotExist:
            return