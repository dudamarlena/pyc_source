# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/GitHub/django_sendgrid_repo/django_sendgrid_parse/models.py
# Compiled at: 2016-09-09 23:43:09
# Size of source mod 2**32: 2708 bytes
from django.db import models
from jsonfield import JSONField
import os
from . import _ugl

def attachments_file_upload(instance, filename):
    fn, ext = os.path.splitext(filename)
    return 'emails/{to}/{id}/{num}{ext}'.format(to=instance.email.to_mailbox, id=instance.email.id, num=instance.number, ext=ext)


class Email(models.Model):
    headers = models.TextField(blank=True, null=True, verbose_name=_ugl('Headers'))
    text = models.TextField(blank=True, null=True, verbose_name=_ugl('Text'))
    html = models.TextField(blank=True, null=True, verbose_name=_ugl('HTML'))
    to_mailbox = models.TextField(blank=False, null=False, verbose_name=_ugl('To'))
    from_mailbox = models.TextField(blank=False, null=False, verbose_name=_ugl('From'))
    cc = models.TextField(blank=True, null=True, verbose_name=_ugl('Carbon Copy'))
    subject = models.TextField(blank=True, null=True, verbose_name=_ugl('Subject'))
    dkim = models.TextField(blank=True, null=True, verbose_name=_ugl('DomainKeys Identified Mail'))
    SPF = models.TextField(blank=True, null=True, verbose_name=_ugl('Sender Policy Framework'))
    envelope = JSONField(blank=True, null=True, verbose_name=_ugl('Envelope'))
    charsets = models.CharField(max_length=255, blank=True, null=True, verbose_name=_ugl('Charsets'))
    spam_score = models.FloatField(blank=True, null=True, verbose_name=_ugl('Spam score'))
    spam_report = models.TextField(blank=True, null=True, verbose_name=_ugl('Spam report'))
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=_ugl('Creation date'))


class Attachment(models.Model):
    number = models.IntegerField(default=1, blank=False, null=False, verbose_name=_ugl("Email's Attachment Number"))
    file = models.FileField(upload_to=attachments_file_upload, blank=False, null=False, verbose_name=_ugl('Attached File'))
    email = models.ForeignKey(Email, blank=False, null=False, related_name='attachments', verbose_name=_ugl('Email Attached To'))

    def filename(self):
        return os.path.basename(self.file.name)