# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django_blogposts/django_blogposts/models/tags.py
# Compiled at: 2018-08-06 11:45:31
# Size of source mod 2**32: 912 bytes
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
__author__ = 'spi4ka'

class Tags(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=100, allow_unicode=True)
    is_moderated = models.BooleanField(_('Is moderated'), default=True)
    da = models.DateTimeField(_('Date of create'), auto_now_add=True)
    de = models.DateTimeField(_('Date of last edit'), auto_now=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['-da']

    def __unicode__(self):
        return '{}'.format(self.__str__())

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('django-blogposts-list') + '?tag=%s' % (self.slug,)