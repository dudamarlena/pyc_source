# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dvs/Dropbox/Code/djangoql/test_project/core/migrations/0003_auto_20171028_1450.py
# Compiled at: 2017-11-09 05:44:46
# Size of source mod 2**32: 1098 bytes
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('core', '0002_book_genre')]
    operations = [
     migrations.CreateModel(name='Publisher',
       fields=[
      (
       'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
      (
       'name', models.CharField(max_length=20)),
      (
       'phone', models.CharField(max_length=10)),
      (
       'address', models.CharField(max_length=70)),
      (
       'site', models.URLField()),
      (
       'email', models.EmailField(max_length=254))]),
     migrations.AddField(model_name='book',
       name='publisher',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='core.Publisher', verbose_name='Publisher'),
       preserve_default=False)]