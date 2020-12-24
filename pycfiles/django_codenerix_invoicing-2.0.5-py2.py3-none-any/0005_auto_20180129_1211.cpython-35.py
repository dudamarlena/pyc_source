# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_invoicing/migrations/0005_auto_20180129_1211.py
# Compiled at: 2018-02-02 06:33:24
# Size of source mod 2**32: 3763 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('codenerix_products', '0008_auto_20180126_1711'),
     ('codenerix_invoicing', '0004_saleslines')]
    operations = [
     migrations.CreateModel(name='Al', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'n', models.IntegerField(blank=True, null=True, verbose_name='Parent pk'))], options={'abstract': False, 
      'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.CreateModel(name='Fa', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'n', models.IntegerField(blank=True, null=True, verbose_name='Parent pk'))], options={'abstract': False, 
      'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.CreateModel(name='P', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'a', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test', to='codenerix_invoicing.Al', verbose_name='A')),
      (
       'f', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test', to='codenerix_invoicing.Fa', verbose_name='F'))], options={'abstract': False, 
      'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.CreateModel(name='Pr', fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
      (
       'updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
      (
       'n', models.IntegerField(blank=True, null=True, verbose_name='Parent pk'))], options={'abstract': False, 
      'default_permissions': ('add', 'change', 'delete', 'view', 'list')}),
     migrations.AddField(model_name='p', name='p', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test', to='codenerix_invoicing.Pr', verbose_name='P')),
     migrations.AddField(model_name='p', name='product_final', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test', to='codenerix_products.ProductFinal', verbose_name='Product'))]