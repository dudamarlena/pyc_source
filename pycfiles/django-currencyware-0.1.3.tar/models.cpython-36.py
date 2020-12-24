# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/.venv/trade/lib/python3.6/site-packages/currencyware/models.py
# Compiled at: 2018-09-14 09:11:28
# Size of source mod 2**32: 4508 bytes
from django.db import models
from django.core.cache import cache
from django.utils.translation import ugettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
from toolware.utils.query import CaseInsensitiveManager, CaseInsensitiveUniqueManager
from .currency import get_all_currencies_prioritized, get_display
from . import defaults as defs

class Currency(models.Model):
    code = models.CharField((_('Code')),
      max_length=3,
      primary_key=True,
      null=False,
      blank=False,
      help_text=(_('Currency code')))
    name = models.CharField((_('Name')),
      max_length=60,
      null=True,
      blank=True,
      help_text=(_('Curreny name (english)')))
    number = models.CharField((_('Number')),
      max_length=3,
      null=True,
      blank=True,
      help_text=(_('Numeric code')))
    unit = models.IntegerField((_('Unit')),
      null=True,
      blank=True,
      help_text=(_('Currency unit')))
    symbol = models.CharField((_('Symbol')),
      max_length=10,
      null=True,
      blank=True,
      help_text=(_('Currency symbol')))
    country = models.CharField((_('Country')),
      max_length=255,
      null=True,
      blank=True,
      help_text=(_('Primary currency in these countries')))
    objects = CaseInsensitiveUniqueManager()
    CASE_INSENSITIVE_FIELDS = [
     'code', 'name']

    @property
    def native_name(self):
        name = get_display(self.code)
        if self.code in name:
            name = self.name
        return name

    def __str__(self):
        return '{} ({})'.format(self.native_name, self.code)

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')


class Rate(models.Model):
    code = models.CharField((_('Code')),
      max_length=3,
      null=False,
      help_text=(_('Currency code')))
    name = models.CharField((_('Name')),
      max_length=100,
      null=True,
      blank=True,
      help_text=(_('Curreny name (english)')))
    rate = models.FloatField((_('Rate')),
      null=False,
      blank=False,
      default=0.0,
      help_text=(_('Currency forex rate')))
    date = models.DateTimeField((_('Date')),
      null=False,
      blank=False,
      help_text=(_("Rate's date")))
    objects = CaseInsensitiveUniqueManager()
    CASE_INSENSITIVE_FIELDS = [
     'code', 'name']

    @property
    def native_name(self):
        name = get_display(self.code)
        if self.code in name:
            name = self.name
        return name

    def __str__(self):
        return '{} ({})'.format(self.native_name, self.code)

    class Meta:
        verbose_name = _('Rate')
        verbose_name_plural = _('Rates')

    @classmethod
    def get_rate(cls, source, target=defs.BASE_CURRENY_CODE):
        """
        Returns value in source to target.
        Example: CAD (source) to EUR (target)
        Rate.get_rate('CAD', 'EUR') => 0.6501663706682155
        50 CAD = 50 * 0.6501663706682155 = 32.50831853341077 EUR
        Default base currency is USD and can be changed via BASE_CURRENY_CODE
        in settings.py
        """
        try:
            source_rate = cls.objects.filter(code=source).latest('date')
            if target == defs.BASE_CURRENY_CODE:
                return 1 / source_rate.rate
            target_rate = cls.objects.filter(code=target).latest('date')
            if source_rate:
                if target_rate:
                    rate = target_rate.rate / source_rate.rate
        except cls.DoesNotExist as err:
            rate = 0.0

        return rate