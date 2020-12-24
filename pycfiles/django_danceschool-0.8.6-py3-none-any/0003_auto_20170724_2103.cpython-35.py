# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/vouchers/migrations/0003_auto_20170724_2103.py
# Compiled at: 2018-03-26 19:55:32
# Size of source mod 2**32: 1878 bytes
from __future__ import unicode_literals
import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('vouchers', '0002_auto_20170717_1642')]
    operations = [
     migrations.RenameField(model_name='voucher', old_name='type', new_name='description'),
     migrations.AlterField(model_name='voucher', name='description', field=models.CharField(blank=True, help_text='For internal use only', max_length=200, null=True, verbose_name='Description (optional)')),
     migrations.AlterField(model_name='voucher', name='disabled', field=models.BooleanField(default=False, help_text='Check this box to disable the voucher entirely.', verbose_name='Voucher Disabled')),
     migrations.AlterField(model_name='voucher', name='maxAmountPerUse', field=models.FloatField(blank=True, help_text='If specified, this will limit the size of a repeated-use voucher.  If unspecified, there is no limit.  Be sure to specify this for publicly advertised voucher codes.', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Max. Amount Per Use')),
     migrations.AlterField(model_name='voucher', name='name', field=models.CharField(help_text='Give a descriptive name that will be used when a customer applies the voucher.', max_length=80, verbose_name='Name')),
     migrations.AlterField(model_name='voucher', name='singleUse', field=models.BooleanField(default=False, verbose_name='Single Use'))]