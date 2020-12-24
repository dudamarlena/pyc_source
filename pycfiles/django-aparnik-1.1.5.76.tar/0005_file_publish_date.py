# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/files/migrations/0005_file_publish_date.py
# Compiled at: 2018-11-10 03:15:27
from __future__ import unicode_literals
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
     ('files', '0004_file_cover')]
    operations = [
     migrations.AddField(model_name=b'file', name=b'publish_date', field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'تاریخ انتشار'))]