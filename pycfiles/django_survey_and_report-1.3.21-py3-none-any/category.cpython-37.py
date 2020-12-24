# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/models/category.py
# Compiled at: 2020-02-22 08:00:49
# Size of source mod 2**32: 805 bytes
from django.db import models
from django.utils.text import slugify
import django.utils.translation as _
from .survey import Survey

class Category(models.Model):
    name = models.CharField((_('Name')), max_length=400)
    survey = models.ForeignKey(Survey, on_delete=(models.CASCADE), verbose_name=(_('Survey')), related_name='categories')
    order = models.IntegerField((_('Display order')), blank=True, null=True)
    description = models.CharField((_('Description')), max_length=2000, blank=True, null=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

    def slugify(self):
        return slugify(str(self))