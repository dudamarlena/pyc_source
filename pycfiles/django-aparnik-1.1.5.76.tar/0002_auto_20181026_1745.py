# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/files/migrations/0002_auto_20181026_1745.py
# Compiled at: 2018-11-05 07:19:14
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('files', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name=b'file', options={b'ordering': [b'-created_at'], b'verbose_name': b'فایل', b'verbose_name_plural': b'فایل ها'}),
     migrations.AlterField(model_name=b'file', name=b'banner', field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name=b'shop_file_banner', to=b'filefields.FileField', verbose_name=b'بنر')),
     migrations.AlterField(model_name=b'file', name=b'description', field=models.TextField(blank=True, null=True, verbose_name=b'توضیحات')),
     migrations.AlterField(model_name=b'file', name=b'file_obj', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name=b'shop_file_obj', to=b'filefields.FileField', verbose_name=b'فایل')),
     migrations.AlterField(model_name=b'file', name=b'is_preview', field=models.BooleanField(default=False, verbose_name=b'پیش نمایش؟'))]