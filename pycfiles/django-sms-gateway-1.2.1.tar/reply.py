# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/matt/Zarloc/Development/trunk/project/apps/django-sms-gateway/sms/models/reply.py
# Compiled at: 2011-12-22 01:07:28
from django.db import models

class Reply(models.Model):
    """
    A reply to a Message.
    """
    content = models.TextField()
    message = models.ForeignKey('sms.Message', related_name='replies')
    date = models.DateTimeField()

    class Meta:
        app_label = 'sms'
        verbose_name_plural = 'replies'