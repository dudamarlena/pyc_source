# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/news/migrations/0003_news_categories.py
# Compiled at: 2018-12-11 08:51:05
from __future__ import unicode_literals
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('categories', '0003_remove_category_pages'),
     ('news', '0002_auto_20181209_2322')]
    operations = [
     migrations.AddField(model_name=b'news', name=b'categories', field=models.ManyToManyField(to=b'categories.Category', verbose_name=b'دسته بندی ها'))]