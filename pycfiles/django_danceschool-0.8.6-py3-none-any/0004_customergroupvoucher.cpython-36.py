# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/vouchers/migrations/0004_customergroupvoucher.py
# Compiled at: 2019-04-03 22:56:33
# Size of source mod 2**32: 1085 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0020_auto_20180808_2247'),
     ('vouchers', '0003_auto_20170724_2103')]
    operations = [
     migrations.CreateModel(name='CustomerGroupVoucher',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'group', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='core.CustomerGroup', verbose_name='Customer group')),
      (
       'voucher', models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='vouchers.Voucher', verbose_name='Voucher'))],
       options={'verbose_name':'Group-specific voucher restriction', 
      'verbose_name_plural':'Group-specific voucher restrictions'})]