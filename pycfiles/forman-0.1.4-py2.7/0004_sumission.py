# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/forman/migrations/0004_sumission.py
# Compiled at: 2017-05-08 12:16:33
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('forman', '0003_auto_20170503_1110')]
    operations = [
     migrations.CreateModel(name=b'Sumission', fields=[
      (
       b'id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name=b'ID')),
      (
       b'columns', models.TextField()),
      (
       b'values', models.TextField()),
      (
       b'survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'forman.Survey'))])]