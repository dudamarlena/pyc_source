# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/discounts/migrations/0006_customerdiscount.py
# Compiled at: 2018-03-26 19:55:30
# Size of source mod 2**32: 1102 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0019_invoice_buyerpayssalestax'),
     ('discounts', '0005_auto_20170830_1159')]
    operations = [
     migrations.CreateModel(name='CustomerDiscount', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Customer', verbose_name='Customer')),
      (
       'discountCombo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discounts.DiscountCombo', verbose_name='Discount'))], options={'verbose_name_plural': 'Customer-specific discount restrictions', 
      'verbose_name': 'Customer-specific discount restriction'})]