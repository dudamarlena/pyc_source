# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/vouchers/migrations/0005_publiceventcategoryvoucher_seriescategoryvoucher_sessionvoucher.py
# Compiled at: 2019-04-03 22:56:33
# Size of source mod 2**32: 2594 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0025_auto_20181109_1631'),
     ('vouchers', '0004_customergroupvoucher')]
    operations = [
     migrations.CreateModel(name='PublicEventCategoryVoucher',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'publicEventCategory', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='core.PublicEventCategory', verbose_name='Public Event Category')),
      (
       'voucher', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='vouchers.Voucher', verbose_name='Voucher'))],
       options={'verbose_name':'Public event category-specific voucher restriction', 
      'verbose_name_plural':'public event Category-specific voucher restrictions'}),
     migrations.CreateModel(name='SeriesCategoryVoucher',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'seriesCategory', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='core.SeriesCategory', verbose_name='Series Category')),
      (
       'voucher', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='vouchers.Voucher', verbose_name='Voucher'))],
       options={'verbose_name':'Series category-specific voucher restriction', 
      'verbose_name_plural':'Series category-specific voucher restrictions'}),
     migrations.CreateModel(name='SessionVoucher',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'session', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='core.EventSession', verbose_name='Event Session')),
      (
       'voucher', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='vouchers.Voucher', verbose_name='Voucher'))],
       options={'verbose_name':'Session-specific voucher restriction', 
      'verbose_name_plural':'Session-specific voucher restrictions'})]