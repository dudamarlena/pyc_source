# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/django_reports/migrations/0002_auto_20170902_1448.py
# Compiled at: 2017-09-02 10:49:19
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('django_reports', '0001_initial')]
    operations = [
     migrations.AddField(model_name=b'report', name=b'description', field=models.CharField(default=b'-', max_length=500, verbose_name=b'Name'), preserve_default=False),
     migrations.AddField(model_name=b'report', name=b'style', field=models.CharField(default=b'pie', max_length=10, verbose_name=b'Name'), preserve_default=False),
     migrations.AddField(model_name=b'report', name=b'title', field=models.CharField(default=b'-', max_length=100, verbose_name=b'Name'), preserve_default=False),
     migrations.AlterField(model_name=b'report', name=b'name', field=models.CharField(unique=True, max_length=10, verbose_name=b'Name'))]