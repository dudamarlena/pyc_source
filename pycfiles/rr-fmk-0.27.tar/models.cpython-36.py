# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rramos/00P/01-dajngo/3d/app/usuarios/models.py
# Compiled at: 2018-03-28 11:45:41
# Size of source mod 2**32: 545 bytes
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=(models.CASCADE))
    department = models.CharField(max_length=100)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_Cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(user=instance)
    instance.cliente.save()