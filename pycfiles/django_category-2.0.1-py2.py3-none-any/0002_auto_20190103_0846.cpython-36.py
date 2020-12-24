# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-category/category/migrations/0002_auto_20190103_0846.py
# Compiled at: 2019-01-04 03:57:04
# Size of source mod 2**32: 1841 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('category', '0001_initial')]
    operations = [
     migrations.AlterField(model_name='category',
       name='sites',
       field=models.ManyToManyField(blank=True, help_text='Limits category scope to selected sites.', to='sites.Site')),
     migrations.AlterField(model_name='category',
       name='slug',
       field=models.SlugField(help_text='Short descriptive unique name for use in urls.', max_length=255, unique=True)),
     migrations.AlterField(model_name='category',
       name='subtitle',
       field=models.CharField(blank=True, default='', help_text='Some titles may be the same and cause confusion in admin UI. A subtitle makes a distinction.', max_length=200, null=True)),
     migrations.AlterField(model_name='category',
       name='title',
       field=models.CharField(help_text='Short descriptive name for this category.', max_length=200)),
     migrations.AlterField(model_name='tag',
       name='categories',
       field=models.ManyToManyField(blank=True, help_text='Categories to which this tag belongs.', to='category.Category')),
     migrations.AlterField(model_name='tag',
       name='slug',
       field=models.SlugField(help_text='Short descriptive unique name for use in urls.', max_length=255, unique=True)),
     migrations.AlterField(model_name='tag',
       name='title',
       field=models.CharField(help_text='Short descriptive name for this tag.', max_length=200))]