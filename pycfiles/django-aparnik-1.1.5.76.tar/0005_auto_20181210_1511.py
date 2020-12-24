# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/news/migrations/0005_auto_20181210_1511.py
# Compiled at: 2018-12-11 08:51:05
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('news', '0004_auto_20181210_1509')]
    operations = [
     migrations.AlterField(model_name=b'news', name=b'cover_images', field=models.ManyToManyField(blank=True, to=b'filefields.FileField', verbose_name=b'Cover Images'))]