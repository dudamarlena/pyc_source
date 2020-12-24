# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-ptdu581r/django-countryware/countryware/models.py
# Compiled at: 2018-08-21 20:41:35
# Size of source mod 2**32: 1372 bytes
from django.db import models
from django.core.cache import cache
from django.utils.translation import ugettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from toolware.utils.query import CaseInsensitiveManager, CaseInsensitiveUniqueManager
from .country import get_all_countries_prioritized, get_display
from . import defaults as defs

class Country(models.Model):
    code = models.CharField((_('Code')),
      max_length=3,
      primary_key=True,
      null=False,
      blank=False,
      help_text=(_('Country code')))
    name = models.CharField((_('Name')),
      max_length=60,
      null=True,
      blank=True,
      help_text=(_('Country name (english)')))
    objects = CaseInsensitiveUniqueManager()
    CASE_INSENSITIVE_FIELDS = [
     'code', 'name']

    @property
    def local_name(self):
        name = get_display(self.code)
        if self.code in name:
            name = self.name
        return name

    def __str__(self):
        return self.local_name

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')