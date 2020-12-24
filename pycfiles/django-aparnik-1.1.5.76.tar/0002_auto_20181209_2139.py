# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/province/migrations/0002_auto_20181209_2139.py
# Compiled at: 2018-12-11 08:51:05
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('province', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name=b'city', options={b'verbose_name': b'City', b'verbose_name_plural': b'Cities'}),
     migrations.AlterModelOptions(name=b'province', options={b'verbose_name': b'Province', b'verbose_name_plural': b'Provinces'}),
     migrations.AlterModelOptions(name=b'shahrak', options={b'verbose_name': b'Shahrak', b'verbose_name_plural': b'Shahraks'}),
     migrations.AlterModelOptions(name=b'town', options={b'verbose_name': b'Town', b'verbose_name_plural': b'Towns'}),
     migrations.AlterField(model_name=b'city', name=b'province', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'province.Province', verbose_name=b'Province')),
     migrations.AlterField(model_name=b'city', name=b'title', field=models.CharField(max_length=255, verbose_name=b'Title')),
     migrations.AlterField(model_name=b'province', name=b'title', field=models.CharField(max_length=100, verbose_name=b'Title')),
     migrations.AlterField(model_name=b'shahrak', name=b'province', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'province.Province', verbose_name=b'Province')),
     migrations.AlterField(model_name=b'shahrak', name=b'title', field=models.TextField(verbose_name=b'Title')),
     migrations.AlterField(model_name=b'town', name=b'city', field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=b'province.City', verbose_name=b'City')),
     migrations.AlterField(model_name=b'town', name=b'title', field=models.CharField(max_length=255, verbose_name=b'Title'))]