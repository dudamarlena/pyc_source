# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/filefields/migrations/0005_auto_20190501_1142.py
# Compiled at: 2019-05-01 03:12:02
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('filefields', '0004_filefield_title')]
    operations = [
     migrations.AddField(model_name=b'filefield', name=b'is_encrypt_needed', field=models.BooleanField(default=False, verbose_name=b'Is encrypt needed?')),
     migrations.AddField(model_name=b'filefield', name=b'is_lock', field=models.BooleanField(default=False, verbose_name=b'Is lock?')),
     migrations.AddField(model_name=b'filefield', name=b'iv', field=models.CharField(blank=True, default=b'', max_length=64, null=True, verbose_name=b'IV')),
     migrations.AddField(model_name=b'filefield', name=b'password', field=models.CharField(blank=True, default=b'', max_length=64, null=True, verbose_name=b'گذرواژه')),
     migrations.AlterField(model_name=b'filefield', name=b'type', field=models.CharField(blank=True, choices=[('M', 'فیلم'), ('V', 'صدا'), ('P', 'پی دی اف'), ('I', 'عکس')], max_length=1, null=True, verbose_name=b'نوع فایل'))]