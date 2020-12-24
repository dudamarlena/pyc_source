# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/signals.py
# Compiled at: 2017-05-03 17:33:20
# Size of source mod 2**32: 675 bytes
from django.db.models.signals import post_save
from django.dispatch import receiver
from google_address import helpers
from google_address.models import Address
from google_address.update import update_address, UpdateThread

@receiver(post_save, sender=Address)
def address_post_save(sender, instance, **kwargs):
    if kwargs.get('raw', False):
        return
    else:
        if helpers.get_settings().get('ASYNC_CALLS', False):
            thread = UpdateThread(instance)
            thread.start()
            return thread
        return update_address(instance)