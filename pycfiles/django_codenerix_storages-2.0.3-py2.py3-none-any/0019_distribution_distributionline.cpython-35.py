# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_storages/migrations/0019_distribution_distributionline.py
# Compiled at: 2018-03-02 10:08:06
# Size of source mod 2**32: 2359 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_invoicing', '0016_purchaseslinealbaran_product_unique'),
     ('codenerix_storages', '0018_auto_20180227_0858')]
    operations = [
     migrations.CreateModel(name='Distribution', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'purchasesorder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='distributions', to='codenerix_invoicing.PurchasesOrder', verbose_name='Order'))], options={'abstract': False, 
      'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.CreateModel(name='DistributionLine', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'quantity', models.FloatField(default=1.0, verbose_name='Quantity')),
      (
       'expected_date', models.DateTimeField(blank=True, null=True, verbose_name='Desired Date')),
      (
       'distribution', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='distribution_lines', to='codenerix_storages.Distribution', verbose_name='Distribution List')),
      (
       'storage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='distribution_lines', to='codenerix_storages.Storage', verbose_name='Storage'))], options={'abstract': False, 
      'default_permissions': ('add', 'change', 'delete', 'view', 'list')})]