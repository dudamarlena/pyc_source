# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/province/migrations/0002_auto_20181209_2139.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 2285 bytes
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
     ('province', '0001_initial')]
    operations = [
     migrations.AlterModelOptions(name='city',
       options={'verbose_name':'City', 
      'verbose_name_plural':'Cities'}),
     migrations.AlterModelOptions(name='province',
       options={'verbose_name':'Province', 
      'verbose_name_plural':'Provinces'}),
     migrations.AlterModelOptions(name='shahrak',
       options={'verbose_name':'Shahrak', 
      'verbose_name_plural':'Shahraks'}),
     migrations.AlterModelOptions(name='town',
       options={'verbose_name':'Town', 
      'verbose_name_plural':'Towns'}),
     migrations.AlterField(model_name='city',
       name='province',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='province.Province', verbose_name='Province')),
     migrations.AlterField(model_name='city',
       name='title',
       field=models.CharField(max_length=255, verbose_name='Title')),
     migrations.AlterField(model_name='province',
       name='title',
       field=models.CharField(max_length=100, verbose_name='Title')),
     migrations.AlterField(model_name='shahrak',
       name='province',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='province.Province', verbose_name='Province')),
     migrations.AlterField(model_name='shahrak',
       name='title',
       field=models.TextField(verbose_name='Title')),
     migrations.AlterField(model_name='town',
       name='city',
       field=models.ForeignKey(on_delete=(django.db.models.deletion.CASCADE), to='province.City', verbose_name='City')),
     migrations.AlterField(model_name='town',
       name='title',
       field=models.CharField(max_length=255, verbose_name='Title'))]