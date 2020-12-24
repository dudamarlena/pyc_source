# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/unleashed/django-smsgateway/smsgateway/models.py
# Compiled at: 2019-04-19 04:31:39
# Size of source mod 2**32: 2993 bytes
from __future__ import absolute_import
from django.db import models
from django.utils.translation import ugettext_lazy
from smsgateway.enums import OPERATOR_CHOICES, OPERATOR_UNKNOWN, GATEWAY_CHOICES, DIRECTION_CHOICES, DIRECTION_INBOUND, PRIORITIES, PRIORITY_MEDIUM, PRIORITY_DEFERRED
from datetime import datetime

class SMS(models.Model):
    sent = models.DateTimeField(default=(datetime.now), verbose_name=(ugettext_lazy('sent')))
    content = models.TextField(verbose_name=(ugettext_lazy('content')), help_text=(ugettext_lazy('SMS content')))
    sender = models.CharField(max_length=32, verbose_name=(ugettext_lazy('sender')), db_index=True)
    to = models.CharField(max_length=32, verbose_name=(ugettext_lazy('receiver')), db_index=True)
    operator = models.IntegerField(choices=OPERATOR_CHOICES, default=OPERATOR_UNKNOWN, verbose_name=(ugettext_lazy('Originating operator')))
    gateway = models.IntegerField(choices=GATEWAY_CHOICES, default=0, verbose_name=(ugettext_lazy('gateway')), help_text=(ugettext_lazy('By which provider the SMS was handled.')))
    backend = models.CharField(max_length=32, db_index=True, default='unknown', verbose_name=(ugettext_lazy('backend')))
    gateway_ref = models.CharField(max_length=64, blank=True, verbose_name=(ugettext_lazy('gateway reference')), help_text=(ugettext_lazy('A reference id for the gateway')))
    direction = models.IntegerField(choices=DIRECTION_CHOICES, default=DIRECTION_INBOUND, verbose_name=(ugettext_lazy('direction')))

    class Meta:
        get_latest_by = 'sent'
        ordering = ('sent', )
        verbose_name = ugettext_lazy('SMS')
        verbose_name_plural = ugettext_lazy('SMSes')

    def __unicode__(self):
        return 'SMS: "{}" from "{}"'.format(self.content, self.sender)


class QueuedSMS(models.Model):
    to = models.CharField(max_length=32, verbose_name=(ugettext_lazy('receiver')))
    signature = models.CharField(max_length=32, verbose_name=(ugettext_lazy('signature')))
    content = models.TextField(verbose_name=(ugettext_lazy('content')), help_text=(ugettext_lazy('SMS content')))
    created = models.DateTimeField(default=(datetime.now))
    using = models.CharField(blank=True, max_length=100, verbose_name=(ugettext_lazy('gateway')), help_text=(ugettext_lazy('Via which provider the SMS will be sent.')))
    priority = models.CharField(max_length=1, choices=PRIORITIES, default=PRIORITY_MEDIUM)
    reliable = models.BooleanField(default=False, blank=True, verbose_name=(ugettext_lazy('is reliable')))

    class Meta:
        get_latest_by = 'created'
        ordering = ('priority', 'created')
        verbose_name = ugettext_lazy('Queued SMS')
        verbose_name_plural = ugettext_lazy('Queued SMSes')

    def defer(self):
        self.priority = PRIORITY_DEFERRED
        self.save()