# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luisza/Escritorio/desarrollo/djreservation/djreservation/signals.py
# Compiled at: 2019-02-19 21:49:51
# Size of source mod 2**32: 670 bytes
"""
Free as freedom will be 5/10/2016

@author: luisza
"""
from __future__ import unicode_literals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from djreservation.email import send_reservation_email
from djreservation.models import Reservation

@receiver(pre_save, sender=Reservation)
def update_product_related(sender, **kwargs):
    instance = kwargs['instance']
    if instance.pk is None:
        return
    status = sender.objects.filter(pk=instance.pk).values('status')[0]['status']
    if instance.status == status:
        return
    send_reservation_email(instance, instance.user)