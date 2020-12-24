# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/davidezanotti/PycharmProjects/buythatgame.com/src/django_easy_currencies/models/Currency.py
# Compiled at: 2014-10-16 04:59:54
from __future__ import unicode_literals
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

class Currency(models.Model):

    class Meta:
        app_label = b'django_easy_currencies'
        db_table = b'django_easy_currencies_currency'
        verbose_name = b'Currency'
        verbose_name_plural = b'Currencies'

    code = models.CharField(max_length=3, validators=[
     MinLengthValidator(3), MaxLengthValidator(3)], help_text=b'Currency code in ISO 4217 format ($ == USD)', db_index=True, primary_key=True)

    def __unicode__(self):
        return self.code

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.code:
            self.code = self.code.strip().upper()
        super(Currency, self).save(force_insert, force_update, using, update_fields)