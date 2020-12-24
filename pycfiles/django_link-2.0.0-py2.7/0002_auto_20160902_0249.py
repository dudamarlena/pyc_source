# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/link/migrations/0002_auto_20160902_0249.py
# Compiled at: 2017-07-06 07:47:29
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('link', '0001_initial')]
    operations = [
     migrations.CreateModel(name=b'ViewParam', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'key', models.CharField(max_length=64)),
      (
       b'value', models.CharField(max_length=256))]),
     migrations.AddField(model_name=b'link', name=b'view_params', field=models.ManyToManyField(blank=True, null=True, to=b'link.ViewParam'))]