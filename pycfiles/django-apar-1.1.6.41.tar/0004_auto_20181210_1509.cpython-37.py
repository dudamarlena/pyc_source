# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/news/migrations/0004_auto_20181210_1509.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 526 bytes
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
     ('news', '0003_news_categories')]
    operations = [
     migrations.AlterField(model_name='news',
       name='categories',
       field=models.ManyToManyField(blank=True, to='categories.Category', verbose_name='\\u062f\\u0633\\u062a\\u0647 \\u0628\\u0646\\u062f\\u06cc \\u0647\\u0627'))]