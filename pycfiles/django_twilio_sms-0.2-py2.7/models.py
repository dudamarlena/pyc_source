# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\django_twilio_sms\models.py
# Compiled at: 2013-06-20 05:49:42
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as tznow

class IncomingSMS(models.Model):
    sms_sid = models.CharField(max_length=34)
    account_sid = models.CharField(max_length=34)
    from_number = models.CharField(max_length=30)
    from_city = models.CharField(max_length=30, default=b'', blank=True)
    from_state = models.CharField(max_length=30, default=b'', blank=True)
    from_zip = models.CharField(max_length=30, default=b'', blank=True)
    from_country = models.CharField(max_length=120, default=b'', blank=True)
    to_number = models.CharField(max_length=30)
    body = models.TextField(max_length=160, default=b'', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _(b'Incoming SMS')
        verbose_name_plural = _(b'Incoming SMS')


class OutgoingSMS(models.Model):
    sms_sid = models.CharField(max_length=34, default=b'', blank=True)
    account_sid = models.CharField(max_length=34, default=b'', blank=True)
    from_number = models.CharField(max_length=30)
    to_number = models.CharField(max_length=30)
    to_parsed = models.CharField(max_length=30, default=b'', blank=True)
    body = models.TextField(max_length=160, default=b'', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default=b'', blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    price_unit = models.CharField(max_length=3, default=b'', blank=True)

    class Meta:
        verbose_name = _(b'Outgoing SMS')
        verbose_name_plural = _(b'Outgoing SMS')

    def save(self, *args, **kwargs):
        if self.status == b'sent' and not self.delivered_at:
            self.delivered_at = tznow()
        super(OutgoingSMS, self).save(*args, **kwargs)