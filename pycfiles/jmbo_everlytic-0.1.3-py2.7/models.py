# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/everlytic/models.py
# Compiled at: 2014-03-14 03:05:27
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from foundry.models import Member
from everlytic import tasks

class EverlyticProfile(models.Model):
    member = models.OneToOneField(Member)
    everlytic_id = models.PositiveIntegerField(null=True, unique=True)

    def __unicode__(self):
        return self.member.__unicode__()


@receiver(post_save, sender=Member)
def member_post_save(sender, instance, **kwargs):
    """ Create an EverlyticProfile and store the Everlytic contact_id in
    the profile. (Use it to delete and update the Contact record).
    Create the Everlytic Contact record if it does not exist.
    Set the subscription status of the Contact on the Everlytic mailing
    list.
    """
    tasks.subscribe_user.delay(instance.id, EverlyticProfile)


@receiver(pre_delete, sender=User)
def member_pre_delete(sender, instance, **kwargs):
    """ Delete the EverlyticProfile and unsubscribe from the appropriate
    mailing list on the Everlytic service. Delete the user from the
    Everlytic database.
    """
    try:
        ep = EverlyticProfile.objects.get(member=instance)
    except EverlyticProfile.DoesNotExist:
        return

    tasks.delete_user.delay(ep.everlytic_id)