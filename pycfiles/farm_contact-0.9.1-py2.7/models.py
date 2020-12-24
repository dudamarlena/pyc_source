# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/contact/models.py
# Compiled at: 2014-04-10 13:30:15
from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

class EnquiryType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Enquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    enquiry_type = models.ForeignKey(EnquiryType)
    message = models.TextField()
    ip = models.IPAddressField(verbose_name='IP Address')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Enquiry')
        verbose_name_plural = _('Enquiries')

    def __unicode__(self):
        return 'Enquiry from %s' % self.name

    def send(self):
        subject = hasattr(settings, 'ENQUIRY_SUBJECT') and settings.ENQUIRY_SUBJECT or 'Contact Form Enquiry'
        message = EmailMessage(subject, render_to_string('contact/enquiry_email.txt', {'obj': self}), settings.DEFAULT_FROM_EMAIL, settings.CONTACT_RECIPIENTS)
        return message.send(True)