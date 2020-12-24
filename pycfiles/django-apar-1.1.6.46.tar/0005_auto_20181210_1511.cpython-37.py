# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/news/migrations/0005_auto_20181210_1511.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 472 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('news', '0004_auto_20181210_1509')]
    operations = [
     migrations.AlterField(model_name='news',
       name='cover_images',
       field=models.ManyToManyField(blank=True, to='filefields.FileField', verbose_name='Cover Images'))]