# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bee/Dev/piu/django/testSite/bee_django_exam/migrations/0020_auto_20180126_1410.py
# Compiled at: 2018-01-26 01:10:24
from __future__ import unicode_literals
import django.core.files.storage
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('bee_django_exam', '0019_auto_20180125_1125')]
    operations = [
     migrations.AddField(model_name=b'grade', name=b'icon', field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/media/exam/cert/icon', location=b'media/exam/cert/icon'), upload_to=b'', verbose_name=b'级别小图标')),
     migrations.AlterField(model_name=b'grade', name=b'cert_image', field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/media/exam/cert/original', location=b'media/exam/cert/original'), upload_to=b'', verbose_name=b'证书图片'))]