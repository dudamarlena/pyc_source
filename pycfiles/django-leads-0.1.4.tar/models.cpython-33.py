# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dnavarro/repos/django-leads/leads/models.py
# Compiled at: 2014-02-26 09:41:22
# Size of source mod 2**32: 1546 bytes
from django.db import models
from django.db.models.signals import post_delete
from django.utils.translation import ugettext_lazy as _

class Register(models.Model):
    __doc__ = '\n    Register model to gather information among the visitors of the lead page\n    '
    email = models.EmailField(unique=True)
    name = models.CharField(_('Name'), max_length=50, blank=True)
    created_on = models.DateTimeField(_('Created on'), auto_now_add=True)
    modified_on = models.DateTimeField(_('Modified on'), auto_now=True)

    class Meta:
        verbose_name = _('Register')
        verbose_name_plural = _('Registers')

    def __str__(self):
        return self.email


def delete_files_handler(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if isinstance(field, models.FileField):
            f = getattr(instance, field.name)
            if f:
                f.delete(save=False)
            else:
                continue


class Newsletter(models.Model):
    __doc__ = '\n    Defines a newsletter to send to regsistered users\n    '
    from_name = models.CharField(_('From name'), max_length=50)
    from_address = models.EmailField(_('From address'))
    subject = models.CharField(_('Subject'), max_length=255)
    html_file = models.FileField(_('HTML file'), upload_to='newsletters')
    created_on = models.DateTimeField(_('Created on'), auto_now_add=True)
    modified_on = models.DateTimeField(_('Modified on'), auto_now=True)

    def __str__(self):
        return self.subject


post_delete.connect(delete_files_handler, Newsletter)