# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davidezanotti/PycharmProjects/buythatgame.com/src/django_easy_currencies/models/CurrencyRate.py
# Compiled at: 2014-10-17 04:23:10
from __future__ import unicode_literals
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

class CurrencyRateManager(models.Manager):

    def get_rate_values(self, currency):
        records = self.select_related().values().filter(original_currency__code=currency)
        rates = {}
        for r in records:
            rates[r[b'target_currency']] = r[b'rate']

        return rates


class CurrencyRate(models.Model):

    class Meta:
        app_label = b'django_easy_currencies'
        db_table = b'django_easy_currencies_rate'
        verbose_name = b'Currency rate'
        verbose_name_plural = b'Currency rates'
        unique_together = (('original_currency', 'target_currency'), )

    original_currency = models.ForeignKey(b'django_easy_currencies.Currency', related_name=b'rates')
    target_currency = models.CharField(max_length=3, validators=[
     MinLengthValidator(3), MaxLengthValidator(3)], db_index=True, editable=False)
    rate = models.DecimalField(max_digits=13, decimal_places=9)
    objects = CurrencyRateManager()

    def __unicode__(self):
        return (b'{0}/{1}: {2}').format(self.original_currency.code, self.target_currency, self.rate)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.target_currency:
            self.target_currency = self.target_currency.strip().upper()
        super(CurrencyRate, self).save(force_insert, force_update, using, update_fields)