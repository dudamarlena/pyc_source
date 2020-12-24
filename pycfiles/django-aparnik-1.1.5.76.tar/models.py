# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/zarinpals/models.py
# Compiled at: 2018-11-13 10:05:31
from __future__ import unicode_literals
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from aparnik.packages.shops.payments.models import Payment

class BankManager(models.Manager):

    def get_queryset(self):
        return super(BankManager, self).get_queryset()

    def get_this_user(self, user):
        if not user.is_authenticated():
            return Bank.objects.none()
        return self.get_queryset().filter(payment__user=user)

    def get_this_success(self):
        return self.get_queryset().filter(Q(ref_id=b'-1'))


class Bank(models.Model):
    TRANSACTION_SUCCESS = 100
    TRANSACTION_SUBMITTED = 101
    TRANSACTION_FAILED = 102
    TRANSACTION_FAILED_BY_USER = -1
    TRANSACTION_WAITING = -2
    TRANSACTION_STATUS = (
     (
      TRANSACTION_SUCCESS, _(b'Success')),
     (
      TRANSACTION_SUBMITTED, _(b'Submitted')),
     (
      TRANSACTION_FAILED, _(b'Failed')),
     (
      TRANSACTION_FAILED_BY_USER, _(b'Cancel By User')),
     (
      TRANSACTION_WAITING, _(b'Waiting for pay')))
    status = models.IntegerField(verbose_name=_(b'Status'), default=-2)
    authority_id = models.CharField(max_length=255, verbose_name=_(b'Authority ID'))
    ref_id = models.CharField(null=True, blank=True, max_length=255, verbose_name=_(b'Bank Reference ID'))
    payment = models.ForeignKey(Payment, verbose_name=_(b'Payment'))
    created_at = models.DateTimeField(verbose_name=_(b'Created At'), auto_now_add=True)
    update_at = models.DateTimeField(verbose_name=_(b'Update At'), auto_now=True)
    objects = BankManager()

    def __unicode__(self):
        return (b'{}').format(self.ref_id)

    def __init__(self, *args, **kwargs):
        super(Bank, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = _(b'Bank')
        verbose_name_plural = _(b'Banks')
        ordering = [b'created_at']

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Bank, self).save(*args, **kwargs)