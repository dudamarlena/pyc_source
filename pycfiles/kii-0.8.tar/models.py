# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/user/models.py
# Compiled at: 2015-01-18 07:28:37
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import Group

class UserData(models.Model):
    """Used to store additional data in user model, without extending
    or replaceing it
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='data')


def create_user_data(sender, instance, created, **kwargs):
    if created:
        ud = UserData(user=instance)
        ud.save()


post_save.connect(create_user_data, sender=settings.AUTH_USER_MODEL)

def add_user_to_default_group(sender, instance, created, **kwargs):
    """Will add all users to default group, except AnonymousUser"""
    if created and not instance.pk == settings.ANONYMOUS_USER_ID:
        group, group_created = Group.objects.get_or_create(name=settings.ALL_USERS_GROUP)
        group.user_set.add(instance)


post_save.connect(add_user_to_default_group, sender=settings.AUTH_USER_MODEL)

def get_all_users_group():
    return Group.objects.get(name=settings.ALL_USERS_GROUP)