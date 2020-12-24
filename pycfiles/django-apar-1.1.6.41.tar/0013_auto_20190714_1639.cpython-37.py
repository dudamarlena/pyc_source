# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/migrations/0013_auto_20190714_1639.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 741 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0012_auto_20190701_0911')]
    operations = [
     migrations.AddField(model_name='filefield',
       name='file_external_url',
       field=models.URLField(blank=True, null=True, verbose_name='url')),
     migrations.AlterField(model_name='filefield',
       name='type',
       field=models.CharField(blank=True, choices=[('M', 'فیلم'), ('V', 'صدا'), ('P', 'پی دی اف'), ('I', 'عکس'), ('L', 'لینک')], max_length=1, null=True, verbose_name='نوع فایل'))]