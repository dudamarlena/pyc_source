# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/bizdir/apps/django-contactware/contactware/models.py
# Compiled at: 2016-08-11 12:49:02
# Size of source mod 2**32: 1252 bytes
from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class ContactMessage(models.Model):
    __doc__ = '\n    Contact Message Model\n    '
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(_('Your name'), max_length=120, blank=False)
    email = models.EmailField(_('Your email address'), max_length=250, blank=False)
    subject = models.CharField(_('Message Subject'), max_length=120, blank=False)
    message = models.TextField(_('Your message'), blank=False, validators=[
     MinLengthValidator(10), MaxLengthValidator(750)])
    referrer = models.CharField(_('referrer'), max_length=254, blank=True)
    identifier = models.CharField(_('Identifier'), max_length=15, blank=True)

    def __str__(self):
        return '{}-{}'.format(self.name, self.email)